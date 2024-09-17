import re
from typing import List

from ..engine.actions import (
    CancelFlow,
    ChangeFlow,
    Clarify,
    CorrectSlots,
    Execute,
    HumanHandoff,
    KnowledgeAnswer,
    Respond,
    SetSlot,
    StartFlow,
)


def convert_string_to_list(input_string):
    """Convert a string to a list of items, splitting on commas not inside parentheses."""
    result = []
    current = ""
    paren_depth = 0
    i = 0
    while i < len(input_string):
        char = input_string[i]
        if char == "(":
            paren_depth += 1
            current += char
        elif char == ")":
            paren_depth -= 1
            current += char
        elif char == "," and paren_depth == 0:
            # Split here
            result.append(current.strip())
            current = ""
        else:
            current += char
        i += 1
    if current:
        result.append(current.strip())
    return result


def translate_policy_to_actions(policy: List[str]):
    """Transform a string to an action instance."""
    pattern = r"^(\w+)(?:\(([^)]*)\))?$"
    actions = []

    for action in policy:
        match = re.match(pattern, action)
        if match:
            action_type = match.group(1)
            args = match.group(2)

            if action_type == "StartFlow":
                actions.append(StartFlow(args))
            elif action_type == "CancelFlow":
                actions.append(CancelFlow())
            elif action_type == "SetSlot":
                slot_name, slot_value = args.split(", ")
                actions.append(SetSlot(slot_name, slot_value))
            elif action_type == "CorrectSlots":
                slot_name, slot_value = args.split(", ")
                actions.append(CorrectSlots(slot_name, slot_value))
            elif action_type == "Clarify":
                actions.append(Clarify(args))
            elif action_type == "KnowledgeAnswer":
                actions.append(KnowledgeAnswer(args))
            elif action_type == "HumanHandoff":
                actions.append(HumanHandoff())
            elif action_type == "ChangeFlow":
                actions.append(ChangeFlow(args))
            elif action_type == "Respond":
                actions.append(Respond(args))
            elif action_type == "Execute":
                actions.append(Execute(args))
            else:
                raise ValueError(f"Unsupported action type: {action_type}")
        else:
            raise ValueError(f"Invalid action format: {action}")

    return actions
