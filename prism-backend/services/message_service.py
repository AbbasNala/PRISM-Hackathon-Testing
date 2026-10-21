def validate_message(speaker, text):
    """Validate a message before it is added to a conversation."""

    if speaker not in ("other", "sign_user"):
        raise ValueError(
            "Speaker must be 'other' or 'sign_user'."
        )

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Message text cannot be empty.")

    return {
        "speaker": speaker,
        "text": text.strip()
    }