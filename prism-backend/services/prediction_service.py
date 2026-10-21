
# PRISM - Context-Aware Prediction Service

PHRASE_PATTERNS = {
    ("HELLO",): [
        "Hello!",
        "Good morning",
        "Nice to meet you"
    ],
    ("HOW",): [
        "How are you?",
        "How can I help?",
        "How is your day?"
    ],
    ("HOW", "ARE"): [
        "How are you?",
        "How are things?"
    ],
    ("THANK",): [
        "Thank you",
        "Thank you very much",
        "Thanks for helping"
    ],
    ("I",): [
        "I am fine",
        "I need help",
        "I want to go"
    ],
    ("I", "NEED"): [
        "I need help",
        "I need water",
        "I need a doctor"
    ],
}

# Temporary rules for responses to common questions.
CONTEXT_PATTERNS = [
   {
    "keywords": ("DRINK",),
    "signs": ("I", "WANT"),
    "suggestions": [
        "I want water",
        "Yes, please",
        "No, thank you"
    ]
},
    {
        "keywords": ("NAME",),
        "signs": ("MY", "NAME"),
        "suggestions": [
            "My name is ...",
            "Nice to meet you",
            "Please tell me your name"
        ]
    },
    {
        "keywords": ("HOW", "ARE", "YOU"),
        "signs": ("I",),
        "suggestions": [
            "I am fine",
            "I am doing well",
            "I am not feeling well"
        ]
    },
]


def predict_phrases(recognized_signs, limit=3, history=None):
    """
    Suggest phrases using recognized signs and conversation history.

    recognized_signs: list of recognized words/sign labels
    history: list of {"speaker": ..., "text": ...}
    limit: maximum number of suggestions
    """
    if not isinstance(recognized_signs, list):
        return []

    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
        return []

    signs = tuple(
        str(sign).strip().upper()
        for sign in recognized_signs
        if str(sign).strip()
    )

    if not signs or limit == 0:
        return []

    # Check whether recent conversation context helps.
    recent_other_text = " ".join(
        message.get("text", "")
        for message in (history or [])
        if isinstance(message, dict)
        and message.get("speaker") == "other"
        and isinstance(message.get("text"), str)
    ).upper()

    for pattern in CONTEXT_PATTERNS:
        context_matches = all(
            keyword in recent_other_text
            for keyword in pattern["keywords"]
        )

        signs_match = all(
            sign in signs
            for sign in pattern["signs"]
        )

        if context_matches and signs_match:
            return pattern["suggestions"][:limit]

    # Fall back to matching the longest recognized sign sequence.
    for length in range(len(signs), 0, -1):
        pattern = signs[-length:]

        if pattern in PHRASE_PATTERNS:
            return PHRASE_PATTERNS[pattern][:limit]

    return []
