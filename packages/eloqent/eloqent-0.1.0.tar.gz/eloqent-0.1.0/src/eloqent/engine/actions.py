"""
This module defines the Action classes used in the dialog engine.
It includes the base Action class and various specialized actions and steps.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Dict

if TYPE_CHECKING:
    from .context import DialogContext, DialogContextStack
else:
    from .context import DialogContext  # type: ignore


class ActionResult:
    def __init__(self, response: str = "", requires_user_input: bool = False):
        self.response = response
        self.requires_user_input = requires_user_input


class Action(ABC):
    """
    Abstract base class for all actions in the dialog engine.
    """

    @abstractmethod
    async def execute(
        self,
        domain: Dict[str, Any],
        context: DialogContext,
        context_stack: DialogContextStack,
    ) -> Dict[str, Any]:
        """
        Execute the action and return the result.

        Args:
            domain: The domain configuration.
            context: The current dialog context.
            context_stack: The stack of dialog contexts.

        Returns:
            A dictionary containing the action result.
        """
        pass


class StartFlow(Action):
    """
    Action to start a new flow in the dialog.
    """

    def __init__(self, name: str):
        """
        Initialize the StartFlow action.

        Args:
            name: The name of the flow to start.
        """
        self.name = name

    async def execute(
        self,
        domain: Dict[str, Any],
        context: DialogContext,
        context_stack: DialogContextStack,
    ) -> ActionResult:
        """
        Execute the StartFlow action.

        Creates a new context for the flow, adds steps to it, and pushes it onto the context stack.

        Args:
            domain: The domain configuration.
            context: The current dialog context.
            context_stack: The stack of dialog contexts.

        Returns:
            A dictionary indicating the action result.
        """
        flow_data = domain.get("flows", {}).get(self.name, {})

        # Create a new context for the flow
        new_context = DialogContext()
        new_context.set_active_flow(self.name)

        # Add steps to the new context
        for step in flow_data.get("steps", []):
            step_type, step_id = next(iter(step.items()))
            if step_type == "respond":
                new_context.add_step(Respond(step_id))
            elif step_type == "execute":
                new_context.add_step(Execute(step_id))
            else:
                print("Not implementend step: %s", step_type)

        # Push the new context onto the stack
        context_stack.push(new_context)

        return ActionResult()


class CancelFlow(Action):
    """
    Action to cancel the current flow.
    """

    async def execute(
        self,
        domain: Dict[str, Any],
        context: DialogContext,
        context_stack: DialogContextStack,
    ) -> ActionResult:
        # Implementation for canceling the current flow
        if not context_stack.is_empty():
            context_stack.pop()
        return ActionResult()


class Respond(Action):
    """
    A step that responds with a predefined message.
    """

    def __init__(self, response_id: str):
        """
        Initialize the RespondStep.

        Args:
            response_id: The ID of the response to use.
        """
        self.response_id = response_id

    async def execute(
        self,
        domain: Dict[str, Any],
        context: DialogContext,
        context_stack: DialogContextStack,
    ) -> ActionResult:
        """
        Execute the Respond step.

        Retrieves the response from the domain and returns it.

        Args:
            domain: The domain configuration.
            context: The current dialog context.
            context_stack: The stack of dialog contexts.

        Returns:
            A dictionary containing the response and whether user input is required.
        """
        responses = domain.get("responses", {}).get(self.response_id, [])
        if responses:
            message = responses[0]  # For simplicity, we're using the first response
            return ActionResult(response=message)
        return ActionResult()


class Request(Action):
    """
    A step that asks a question and waits for user input.
    """

    def __init__(self, question_id: str):
        """
        Initialize the AskQuestionStep.

        Args:
            question_id: The ID of the question to ask.
        """
        self.question_id = question_id

    async def execute(
        self,
        domain: Dict[str, Any],
        context: DialogContext,
        context_stack: DialogContextStack,
    ) -> ActionResult:
        """
        Execute the AskQuestionStep.

        Retrieves the question from the domain and returns it, indicating that user input is required.

        Args:
            domain: The domain configuration.
            context: The current dialog context.
            context_stack: The stack of dialog contexts.

        Returns:
            A dictionary containing the question and indicating that user input is required.
        """
        questions = domain.get("questions", {}).get(self.question_id, [])
        if questions:
            question = questions[0]  # For simplicity, we're using the first question
            return ActionResult(response=question, requires_user_input=True)
        return ActionResult()


class SetSlot(Action):
    """
    Action to set a slot value.
    """

    def __init__(self, slot_name: str, slot_value: Any):
        """
        Initialize the SetSlot action.

        Args:
            slot_name: The name of the slot to set.
            slot_value: The value to set the slot to.
        """
        self.slot_name = slot_name
        self.slot_value = slot_value

    async def execute(
        self,
        domain: Dict[str, Any],
        context: DialogContext,
        context_stack: DialogContextStack,
    ) -> ActionResult:
        """
        Execute the SetSlot action.

        Sets the slot value in the current context.

        Args:
            domain: The domain configuration.
            context: The current dialog context.
            context_stack: The stack of dialog contexts.
        """
        context.update_slot(self.slot_name, self.slot_value)
        return ActionResult()


class CorrectSlots(Action):
    """
    Action to correct a slot value.
    """

    def __init__(self, slot_name: str, slot_value: Any):
        """
        Initialize the CorrectSlots action.

        Args:
            slot_name: The name of the slot to correct.
            slot_value: The value to correct the slot to.
        """
        self.slot_name = slot_name
        self.slot_value = slot_value

    async def execute(
        self,
        domain: Dict[str, Any],
        context: DialogContext,
        context_stack: DialogContextStack,
    ) -> ActionResult:
        """
        Execute the CorrectSlots action.

        Corrects the slot value in the current context.

        Args:
            domain: The domain configuration.
            context: The current dialog context.
            context_stack: The stack of dialog contexts.
        """
        context.update_slot(self.slot_name, self.slot_value)
        return ActionResult()


class Clarify(Action):
    """Action to request clarification from the user."""

    def __init__(self, clarification_message: str):
        """
        Initialize the Clarify action.

        Args:
            clarification_message: The message to ask for clarification.
        """
        self.clarification_message = clarification_message

    async def execute(
        self,
        domain: Dict[str, Any],
        context: DialogContext,
        context_stack: DialogContextStack,
    ) -> ActionResult:
        """
        Execute the Clarify action.

        Returns:
            A dictionary containing the clarification message and indicating that user input is required.
        """
        return ActionResult(
            response=self.clarification_message, requires_user_input=True
        )


class KnowledgeAnswer(Action):
    """Action to provide a knowledge-based answer."""

    def __init__(self, answer: str):
        """
        Initialize the KnowledgeAnswer action.

        Args:
            answer: The answer to provide.
        """
        self.answer = answer

    async def execute(
        self,
        domain: Dict[str, Any],
        context: DialogContext,
        context_stack: DialogContextStack,
    ) -> ActionResult:
        """
        Execute the KnowledgeAnswer action.

        Returns:
            A dictionary containing the answer and indicating that user input is not required.
        """
        return ActionResult(response=self.answer)


class HumanHandoff(Action):
    """Action to hand off the conversation to a human agent."""

    async def execute(
        self,
        domain: Dict[str, Any],
        context: DialogContext,
        context_stack: DialogContextStack,
    ) -> ActionResult:
        """
        Execute the HumanHandoff action.

        Returns:
            A dictionary indicating that the conversation has been handed off to a human agent.
        """
        return ActionResult(response="Transferring to a human agent...")


class ChangeFlow(Action):
    """Action to change to a new flow."""

    def __init__(self, new_flow: str):
        """
        Initialize the ChangeFlow action.

        Args:
            new_flow: The name of the new flow to change to.
        """
        self.new_flow = new_flow

    async def execute(
        self,
        domain: Dict[str, Any],
        context: DialogContext,
        context_stack: DialogContextStack,
    ) -> ActionResult:
        """
        Execute the ChangeFlow action.

        Changes to a new flow in the current context.

        Args:
            domain: The domain configuration.
            context: The current dialog context.
            context_stack: The stack of dialog contexts.
        """
        if not context_stack.is_empty():
            context_stack.pop()
        new_context = DialogContext()
        new_context.set_active_flow(self.new_flow)
        context_stack.push(new_context)
        return ActionResult()


class Execute(Action):
    """
    A step that executes a custom action.
    """

    def __init__(self, action_id: str):
        """
        Initialize the Execute step.

        Args:
            action_id: The ID of the action to execute.
        """
        self.action_id = action_id

    async def execute(
        self,
        domain: Dict[str, Any],
        context: DialogContext,
        context_stack: DialogContextStack,
    ) -> ActionResult:
        """
        Execute the custom action.

        Retrieves the action from the domain and executes it.

        Args:
            domain: The domain configuration.
            context: The current dialog context.
            context_stack: The stack of dialog contexts.

        Returns:
            A dictionary containing the result of the action execution.
        """
        actions = domain.get("actions", {})
        action = actions.get(self.action_id)
        if not action:
            return ActionResult(response=f"Error: Action '{self.action_id}' not found")

        try:
            # Get the action handler
            handler = self._get_action_handler(action)

            # Execute the action
            return await handler(action, context, domain)
        except Exception as e:
            # Log the error (you should implement proper logging)
            print(f"Error executing action '{self.action_id}': {str(e)}")
            return ActionResult(response=f"Error executing action: {self.action_id}")

    def _get_action_handler(self, action: Dict[str, Any]) -> Callable:
        """
        Get the appropriate handler for the action type.
        You can extend this method to support different types of actions.
        """
        action_type = action.get("type", "default")
        if action_type == "http":
            return self._handle_http_call
        elif action_type == "code":
            return self._handle_code_exection
        # Add more action types here
        return self._handle_default_action

    async def _handle_http_call(
        self, action: Dict[str, Any], context: DialogContext, domain: Dict[str, Any]
    ) -> ActionResult:
        # Implement API call logic here
        # This is a placeholder implementation
        return ActionResult(
            response=f"API call to {action.get('endpoint', 'unknown')} executed"
        )

    async def _handle_code_exection(
        self, action: Dict[str, Any], context: DialogContext, domain: Dict[str, Any]
    ) -> ActionResult:
        # Implement code execution logic here
        return ActionResult(response=f"Executed code: {self.action_id}")

    async def _handle_default_action(
        self, action: Dict[str, Any], context: DialogContext, domain: Dict[str, Any]
    ) -> ActionResult:
        # Implement default action logic here
        return await self._handle_code_exection(action, context, domain)
