
from flask import Blueprint, jsonify, request
from services.recognition_service import recognize_signs

from services.conversation_service import (
    create_conversation,
    add_message,
    get_history,
)
from services.prediction_service import predict_phrases

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "project": "PRISM"
    }), 200


@api.route("/conversation/start", methods=["POST"])
def start_conversation():
    session_id = create_conversation()

    return jsonify({
        "success": True,
        "session_id": session_id
    }), 201


@api.route("/conversation/message", methods=["POST"])
def receive_message():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400

    session_id = data.get("session_id")
    speaker = data.get("speaker")
    message_text = data.get("text")

    if not isinstance(session_id, str) or not session_id.strip():
        return jsonify({"error": "Session ID is required"}), 400

    if speaker not in ("other", "sign_user"):
        return jsonify({
            "error": "Speaker must be 'other' or 'sign_user'"
        }), 400

    if not isinstance(message_text, str) or not message_text.strip():
        return jsonify({"error": "Message text is required"}), 400

    try:
        message = add_message(
            session_id,
            speaker,
            message_text
        )
    except KeyError:
        return jsonify({"error": "Conversation not found"}), 404
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "success": True,
        "message": message
    }), 201


@api.route("/conversation/history/<session_id>", methods=["GET"])
def conversation_history(session_id):
    try:
        history = get_history(session_id)
    except KeyError:
        return jsonify({"error": "Conversation not found"}), 404

    return jsonify({
        "session_id": session_id,
        "history": history
    }), 200


@api.route("/recognize", methods=["POST"])
def recognize():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400

    landmarks = data.get("landmarks")

    if not isinstance(landmarks, list) or not landmarks:
        return jsonify({"error": "Landmarks are required"}), 400

    try:
        signs = recognize_signs(landmarks)

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except NotImplementedError as error:
        return jsonify({
            "error": str(error)
        }), 501

    return jsonify({
        "success": True,
        "recognized_signs": signs
    }), 200



@api.route("/suggest", methods=["POST"])
def suggest():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400

    signs = data.get("recognized_signs")
    session_id = data.get("session_id")

    if not isinstance(signs, list) or not signs:
        return jsonify({
            "error": "Recognized signs are required"
        }), 400

    if not isinstance(session_id, str) or not session_id.strip():
        return jsonify({
            "error": "Session ID is required"
        }), 400

    try:
        history = get_history(session_id)
    except KeyError:
        return jsonify({
            "error": "Conversation not found"
        }), 404

    suggestions = predict_phrases(
        signs,
        limit=3,
        history=history
    )

    return jsonify({
        "success": True,
        "session_id": session_id,
        "suggestions": suggestions
    }), 200



@api.route("/confirm", methods=["POST"])
def confirm():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400

    session_id = data.get("session_id")
    message = data.get("confirmed_message")

    if not isinstance(session_id, str) or not session_id.strip():
        return jsonify({"error": "Session ID is required"}), 400

    if not isinstance(message, str) or not message.strip():
        return jsonify({
            "error": "A confirmed message is required"
        }), 400

    try:
        saved_message = add_message(
            session_id,
            "sign_user",
            message.strip()
        )
    except KeyError:
        return jsonify({"error": "Conversation not found"}), 404
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "success": True,
        "confirmed_message": saved_message["text"],
        "message": saved_message
    }), 200

