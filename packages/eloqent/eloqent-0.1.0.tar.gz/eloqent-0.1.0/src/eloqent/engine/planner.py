"""Dialog understanding module that predicts the next set of actions in the dialog policy."""

from __future__ import annotations

from typing import Any, Dict, List

import dspy

from ..utils.helpers import convert_string_to_list
from .constants import AVAILABLE_ACTIONS_FOR_PREDICTION


class DialogPolicy(dspy.Signature):
    """You are dialog policy that predicts the next set of actions in the dialog.

    Given the tasks to be done, the available actions, the current state of the dialog,
    the conversation history, and the latest message from the user, predict the next
    set of actions in the policy."""

    tasks = dspy.InputField(
        description="may contain relevant tasks to be done.",
        format=lambda x: "\n".join(x) if isinstance(x, list) else x,
    )
    conversation_history = dspy.InputField(
        description="contains the transcript of the conversation.",
        format=lambda x: "\n".join(x) if isinstance(x, list) else x,
    )
    current_state = dspy.InputField(
        description=(
            """the current state of the dialog. It may contain the current task, """
            """the slots filled or needed, etc."""
        ),
        format=lambda x: str(x) if isinstance(x, dict) else x,
    )
    available_actions = dspy.InputField(
        description="the actions that the assistant can take.",
    )
    users_latest_message = dspy.InputField(
        description="the latest message from the user.",
    )
    policy = dspy.OutputField(
        description=(
            """the policy to be executed by the assistant. A list of actions from the """
            """available actions separated by comma if more than one are required."""
        ),
        # format=convert_string_to_list,
    )


class RephrasedUserMessage(dspy.Signature):
    """Rephrase the user message in a self-contained sentence in first person."""

    conversation_history = dspy.InputField(
        description="contains the transcript of the conversation.",
        format=lambda x: "\n".join(x) if isinstance(x, list) else x,
    )
    users_latest_message = dspy.InputField(
        description="the latest message from the user."
    )
    rephrased_message = dspy.OutputField(description="the rephrased message.")


class DialogPlanner(dspy.Module):
    """Dialog understanding that predicts next set of actions."""

    def __init__(self, num_actions: int = 10):
        super().__init__()

        self.rephrase_user_message = dspy.ChainOfThought(RephrasedUserMessage)
        self.retrieve = dspy.Retrieve(k=num_actions)
        self.generate_policy = dspy.ChainOfThought(DialogPolicy)

    def forward(self, conversation_history, current_state, users_latest_message):
        """
        Predict the next set of actions in the dialog policy.

        Args:
            conversation_history: The transcript of the conversation.
            current_state: The current state of the dialog.
            users_latest_message: The latest message from the user.

        Returns:
            A list of predicted actions.
        """
        rephraser = self.rephrase_user_message(
            conversation_history=conversation_history,
            users_latest_message=users_latest_message,
        )
        retrieved_tasks = self.retrieve(rephraser.rephrased_message).passages
        prediction = self.generate_policy(
            tasks=retrieved_tasks,
            conversation_history=conversation_history,
            current_state=current_state,
            available_actions=AVAILABLE_ACTIONS_FOR_PREDICTION,
            users_latest_message=users_latest_message,
        )

        actions = self._parse_actions(prediction.policy)
        valid_actions = self._validate_actions(actions)
        return valid_actions

    def _parse_actions(self, policy: str) -> List[str]:
        """
        Parse the policy string into a list of actions.

        Args:
            policy: The policy string to parse.

        Returns:
            A list of parsed actions.
        """
        return convert_string_to_list(policy)

    def _validate_actions(self, actions: List[str]) -> List[str]:
        """
        Validate the actions against the available actions.

        Args:
            actions: The list of actions to validate.

        Returns:
            A list of valid actions.
        """
        valid_actions = []
        available_action_names = [
            action.split("(")[0]
            for action in AVAILABLE_ACTIONS_FOR_PREDICTION.split("\n")
            if action.strip()
        ]
        for action in actions:
            action_name = action.split("(")[0]
            if action_name in available_action_names:
                valid_actions.append(action)
            else:
                print(f"Warning: '{action_name}' is not a valid action.")
        return valid_actions


class DummyDialogPlanner:
    """A dummy dialog planner for testing purposes."""

    def __init__(self):
        """Initialize the DummyDialogPlanner with predefined responses."""
        self.predefined_responses = [
            ["StartFlow(greeting)"],
            ["SetSlot(user_name, 'John Doe')"],
            ["Clarify(greeting, goodbye)"],
            ["CancelFlow()"],
        ]
        self.response_index = 0

    def __call__(
        self,
        conversation_history: List[Dict[str, Any]],
        current_state: Dict[str, Any],
        users_latest_message: str,
    ):
        """
        Generate a dummy response based on predefined actions.

        Args:
            conversation_history: The transcript of the conversation.
            current_state: The current state of the dialog.
            users_latest_message: The latest message from the user.

        Returns:
            A dummy prediction object with a policy attribute.
        """

        if "weather" in users_latest_message:
            return type("Prediction", (), {"policy": ["Execute(get_weather)"]})()
        elif "goodbye" in users_latest_message:
            return type(
                "Prediction", (), {"policy": ["CancelFlow()", "Respond(farewell)"]}
            )()
        elif "name" in users_latest_message:
            return type(
                "Prediction", (), {"policy": ["SetSlot(user_name, 'John Doe')"]}
            )()
        elif "greeting" in users_latest_message:
            return type("Prediction", (), {"policy": ["Respond(greet)"]})()
        else:
            return type("Prediction", (), {"policy": ["Respond(farewell)"]})()
