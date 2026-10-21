\# PRISM Backend



PRISM is a backend API for sign-language communication, conversation history, contextual phrase suggestions, and confirmed message handling.



\## Requirements

\- Python 3.11 or compatible version

\- pip



\## Setup



Open PowerShell in the project folder:



```powershell

cd C:\\Users\\Aditya\\Desktop\\prism-backend

```



Create a virtual environment:



```powershell

python -m venv venv

```



Activate it:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

python -m pip install -r requirements.txt

```



\## Run the server



```powershell

python app.py

```



The backend runs at `http://127.0.0.1:5000`.



Keep the terminal running while using the API.



\## Available endpoints



\- `GET /api/health` — Check backend status.

\- `POST /api/conversation/start` — Create a conversation session.

\- `POST /api/conversation/message` — Add a message.

\- `GET /api/conversation/history/<session\_id>` — Retrieve conversation history.

\- `POST /api/suggest` — Generate contextual phrase suggestions.

\- `POST /api/confirm` — Save a user-confirmed message.

\- `POST /api/recognize` — Recognition endpoint; the actual sign-recognition model is not integrated yet.



\## Important notes



\- Use the same `session\_id` for all requests belonging to one conversation.

\- Conversation data is currently stored in memory and is lost when the server restarts.

\- Phrase suggestions currently use predefined rules, not a trained prediction model.

\- Sign recognition is not yet connected.

\- The frontend and recognition model must follow the request/response formats agreed upon by the team.

