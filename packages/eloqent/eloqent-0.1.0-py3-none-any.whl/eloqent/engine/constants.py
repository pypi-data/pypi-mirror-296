"""Constants for the nest project."""

AVAILABLE_ACTIONS_FOR_PREDICTION = """
- StartFlow(flow_name): Start a new flow.
- CancelFlow(): Cancel the current flow.
- SetSlot(slot_name, value): Set a slot to a given value.
- CorrectSlots(slot_name, new_value): Change the value of a given slot to a new value.
- Clarify(flow_name1, flow_name2, ..., flow_nameN): Ask for clarification.
- KnowledgeAnswer(message): Reply with a knowledge-based free-form answer.
- HumanHandoff(): Hand off the conversation to a human.
- ChangeFlow(flow_name): Change to a different flow.
"""
