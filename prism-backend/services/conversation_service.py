from services.message_service import validate_message
# PRISM - Conversation Context Service

from uuid import uuid4
from threading import Lock

# Temporary in-memory conversation storage.
# Conversations will reset when the backend restarts.
_conversations = {}
_lock = Lock()


def create_conversation():
    """Create a new conversation and return its session ID."""
    session_id = str(uuid4())

    with _lock:
        _conversations[session_id] = []

    return session_id


def add_message(session_id, speaker, text):
    message = validate_message(speaker, text)

    with _lock:
        if session_id not in _conversations:
            raise KeyError("Conversation not found.")

        _conversations[session_id].append(message)
        return message.copy()

def get_history(session_id, limit=10):
    """Return the most recent messages in conversation order."""
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("Limit must be a positive integer.")

    with _lock:
        if session_id not in _conversations:
            raise KeyError("Conversation not found.")

        return [
            message.copy()
            for message in _conversations[session_id][-limit:]
        ]


def clear_conversation(session_id):
    """Clear the messages while keeping the session ID valid."""
    with _lock:
        if session_id not in _conversations:
            raise KeyError("Conversation not found.")

        _conversations[session_id] = []
