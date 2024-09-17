"""
This module defines the dialog context and related classes for managing conversation state.
"""

from __future__ import annotations

import copy
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from .actions import Action


class DialogState(Enum):
    """Enum representing the possible states of a dialog."""

    WAITING_FOR_USER = "waiting_for_user"
    PROCESSING = "processing"
    WAITING_FOR_TASK = "waiting_for_task"


class DialogContext:
    """
    Represents the context of a dialog, including its state, active flow, and slot values.
    """

    def __init__(self):
        self.active_flow: Optional[str] = None
        self.slots: Dict[str, Any] = {}
        self.dialog_state: DialogState = DialogState.WAITING_FOR_USER
        self.pending_steps: List[Action] = []

    def is_current_flow_completed(self) -> bool:
        """Check if the current flow is completed."""
        return len(self.pending_steps) == 0 and self.active_flow is not None

    def set_active_flow(self, flow: Optional[str]) -> None:
        """Set the active flow for the dialog."""
        self.active_flow = flow

    def add_step(self, step: Action):
        """Add a step to the pending steps list."""
        self.pending_steps.append(step)

    def update_slot(self, slot_name: str, value: Any):
        """Update a slot with a new value."""
        self.slots[slot_name] = value

    def clear_slots(self):
        """Clear all slots in the context."""
        self.slots = {}

    def update_state(self, state: DialogState):
        """Update the dialog state."""
        self.dialog_state = state

    def get_context(self) -> Dict[str, Any]:
        """Get a dictionary representation of the context."""
        return {
            "active_flow": self.active_flow,
            "slots": self.slots,
            "dialog_state": self.dialog_state.value,
        }

    def copy(self):
        """Create a deep copy of the dialog context."""
        new_context = DialogContext()
        new_context.active_flow = self.active_flow
        new_context.slots = copy.deepcopy(self.slots)
        new_context.dialog_state = self.dialog_state
        return new_context


class DialogContextStack:
    """
    A stack data structure for managing multiple dialog contexts.
    """

    def __init__(self):
        self.stack: List[DialogContext] = []

    def push(self, context: DialogContext):
        """Push a dialog context onto the stack."""
        self.stack.append(context)

    def pop(self) -> DialogContext:
        """Pop and return the top dialog context from the stack."""
        if not self.is_empty():
            return self.stack.pop()
        raise IndexError("Stack is empty")

    def peek(self) -> DialogContext:
        """Return the top dialog context without removing it from the stack."""
        if not self.is_empty():
            return self.stack[-1]
        raise IndexError("Stack is empty")

    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self.stack) == 0

    def size(self) -> int:
        """Return the number of dialog contexts in the stack."""
        return len(self.stack)
