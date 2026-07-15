# WebSocket Chat Application

This project is a WebSocket-based chat application built using FastAPI and Jinja2 templates. The application allows multiple clients to connect, send messages, and receive messages in real-time.

## Features

- Real-time messaging using WebSockets
- Unique client IDs for each connection
- Message history for new connections
- Responsive UI with Tailwind CSS
- Auto-scroll to the latest message

## Requirements

- Python 3.12+
- FastAPI
- Jinja2
- WebSockets

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ameyer117/FastAPI_Websockets.git
    cd websocket-chat
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Sync the required dependencies using `uv`:
    ```sh
    uv sync
    ```

## Running the Application

1. Start the FastAPI server:
    ```sh
    uvicorn main:app --reload
    ```

2. Open your web browser and navigate to `http://localhost:8000` to access the chat application.

## Project Structure

- `main.py`: The main FastAPI application file.
- `templates/index.html`: The HTML template for the chat application.
- `.venv/`: The virtual environment directory.
- `requirements.txt`: The list of dependencies.

## Usage

- Open the chat application in your browser.
- Enter a message in the input field and click "Send" or press "Enter" to send the message.
- Messages from other clients will appear in the message area.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.