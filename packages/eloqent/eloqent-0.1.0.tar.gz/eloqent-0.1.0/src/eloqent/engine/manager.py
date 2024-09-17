"""Module for managing dialog interactions and executing actions based on user input."""

from typing import Any, AsyncGenerator, Dict, List

from ..utils.helpers import translate_policy_to_actions
from .actions import Action, ActionResult, StartFlow
from .context import DialogContext, DialogContextStack
from .planner import DialogPlanner


class DialogManager:
    """
    Manages the dialog flow, processes user messages, and executes actions.

    This class is responsible for maintaining the dialog context, processing user
    input, and coordinating the execution of dialog actions.
    """

    def __init__(
        self,
        domain: Dict[str, Any],
        planner: DialogPlanner,
        dialog_context: DialogContext,
    ):
        """
        Initialize the DialogManager.

        Args:
            domain: The domain configuration for the dialog system.
            planner: The dialog planner used to generate action policies.
            dialog_context: The initial dialog context.
        """
        self.domain = domain
        self.planner = planner
        self.context_stack = DialogContextStack()
        self.context_stack.push(dialog_context)
        self.history: List[Dict[str, Any]] = []

    @property
    def dialog_context(self):
        """Return the current dialog context."""
        return self.context_stack.peek()

    async def process_user_message(
        self, user_message: str
    ) -> AsyncGenerator[str, None]:
        """
        Process a user message and generate responses.

        Args:
            user_message: The message from the user.

        Yields:
            Generated responses based on the processed user message.
        """
        self.history.append({"role": "user", "content": user_message})

        current_context = self.dialog_context.get_context()

        prediction = self.planner(
            conversation_history=self.history.copy(),
            current_state=current_context,
            users_latest_message=user_message,
        )
        actions = translate_policy_to_actions(prediction.policy)

        async for response in self._execute_actions(actions):
            yield response
            self.history.append({"role": "assistant", "content": response})

        if self.dialog_context.is_current_flow_completed():
            self.context_stack.pop()
            if self.context_stack.is_empty():
                self.context_stack.push(DialogContext())

    async def _execute_actions(
        self, actions: List[Action]
    ) -> AsyncGenerator[str, None]:
        """
        Execute a list of actions and yield responses.

        Args:
            actions: List of actions to execute.

        Yields:
            Responses generated from executing the actions.
        """
        for action in actions:
            result = await self._execute_action(action)
            if result.response:
                yield result.response

            if isinstance(action, StartFlow):
                while self.dialog_context.pending_steps:
                    step = self.dialog_context.pending_steps.pop(0)
                    step_result = await self._execute_action(step)

                    if step_result and step_result.response:
                        yield step_result.response

                    if step_result and step_result.requires_user_input:
                        break

            if result.requires_user_input:
                break

    async def _execute_action(self, action: Action) -> ActionResult:
        """
        Execute a single action.

        Args:
            action: The action to execute.

        Returns:
            A dictionary containing the result of the action execution.
        """
        return await action.execute(
            self.domain, self.dialog_context, self.context_stack
        )
