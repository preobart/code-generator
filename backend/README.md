## Setup

1. Create a Python virtual environment in the backend folder:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Install backend dependencies:
    ```bash
    pip install -r backend/requirements.txt
    ```
3. Run the Flask backend:
    ```bash
    flask --app backend/server.py run
    ```
4. Open the frontend in your browser