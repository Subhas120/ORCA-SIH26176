"""
ORCA Conversation Context Manager

Maintains short-term conversation state for the M1 agent layer.
"""

from copy import deepcopy


CONTEXT_FIELDS = [
    "location",
    "date",
    "time",
    "activity",
]


class ConversationContext:
    """
    Stores the latest known query entities for a conversation.
    """

    def __init__(self):
        self._state = {
            field: None
            for field in CONTEXT_FIELDS
        }

    def update(self, entities: dict) -> dict:
        """
        Update stored context using non-empty entity values.

        Existing values are preserved when the new query
        does not provide a value.
        """

        for field in CONTEXT_FIELDS:
            value = entities.get(field)

            if value is not None and value != "":
                self._state[field] = value

        return self.get()

    def get(self) -> dict:
        """
        Return a copy of the current conversation context.
        """

        return deepcopy(self._state)

    def fill_missing(self, entities: dict) -> dict:
        """
        Fill missing entities from the stored conversation context.

        Explicit values from the current query always take priority.
        """

        result = {}

        for field in CONTEXT_FIELDS:
            current_value = entities.get(field)

            if current_value is not None and current_value != "":
                result[field] = current_value
            else:
                result[field] = self._state[field]

        return result

    def clear(self) -> None:
        """
        Clear all stored conversation context.
        """

        for field in CONTEXT_FIELDS:
            self._state[field] = None
