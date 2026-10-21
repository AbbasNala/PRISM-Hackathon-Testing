\# PRISM Backend API Contract



Base URL: `http://127.0.0.1:5000`



All request bodies use JSON.



\## 1. Health Check

GET `/api/health`



Checks whether the backend is running.



\## 2. Start Conversation

POST `/api/conversation/start`



No request body required.



Response:

\- `success`

\- `session\_id`



Use this session ID for every request belonging to the same conversation.



\## 3. Add Message

POST `/api/conversation/message`



Request:

\- `session\_id`: string

\- `speaker`: `"other"` or `"sign\_user"`

\- `text`: string



Stores a message in conversation history.



Use `"other"` for the speaking participant and `"sign\_user"` for the sign-language participant.



\## 4. Get Conversation History

GET `/api/conversation/history/<session\_id>`



Returns the session ID and recent messages.



\## 5. Generate Suggestions

POST `/api/suggest`



Request:

\- `session\_id`: string

\- `recognized\_signs`: array of strings



Response:

\- `success`

\- `session\_id`

\- `suggestions`: array of up to three suggested phrases



Suggestions are currently rule-based. They are not automatically saved as messages.



\## 6. Confirm Message

POST `/api/confirm`



Request:

\- `session\_id`: string

\- `confirmed\_message`: string



Saves the confirmed reply as a `sign\_user` message.



Do not separately add the same confirmed reply through `/api/conversation/message`, or it may be duplicated.



\## 7. Sign Recognition

POST `/api/recognize`



Current request:

\- `landmarks`: non-empty array



The recognition service interface exists, but the actual sign-recognition model is not connected yet. The model developer and backend developer must agree on the final input and output formats before integration.



\## Important Notes

\- All requests for one conversation must use the same session ID.

\- Conversation history is currently stored in memory and is lost when the Flask server restarts.

\- The frontend should handle suggestions separately from confirmed conversation messages.

\- The browser frontend must use the correct backend URL for its environment. `127.0.0.1` works locally, but a deployed frontend will need a reachable backend URL.



