from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from inspect import signature
import json

# State dictionary to hold application-wide variables
app_state = {}


# Lifespan event handler
@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup: Initialize variables
    app_state["active_connections"] = []
    app_state["client_id_counter"] = 0
    app_state["message_history"] = []
    print("Application starting up... 🚀")

    yield  # Application runs here

    # After the yield, the application is shutting down, clean up resources here
    # Shutdown: Clean up connections
    for connection in app_state["active_connections"]:
        try:
            await connection["websocket"].close()
            print(f"Closed connection for Client {connection['client_id']}")
        except Exception as e:
            print(f"Error closing connection for Client {connection['client_id']}: {e}")
    app_state["active_connections"].clear()
    print("Application shutting down...")


# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")


# Serve the chat HTML page
@app.get("/")
async def get(request: Request):
    params = signature(templates.TemplateResponse).parameters
    if "request" in params:
        return templates.TemplateResponse(request, "index.html", {"app_name": "Chat App"})
    return templates.TemplateResponse("index.html", {"request": request, "app_name": "Chat App"})


# Broadcast function using app_state
async def broadcast(message: str):
    """
    Broadcast a message to all active WebSocket connections.
    """
    dead_connections = []
    for connection in app_state["active_connections"]:
        try:
            await connection["websocket"].send_text(message)
        except Exception as exc:
            print(f"Error sending message to Client {connection['client_id']}: {exc}")
            dead_connections.append(connection)
    for dead in dead_connections:
        app_state["active_connections"].remove(dead)


# WebSocket endpoint for chat
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Assign a unique client ID
    app_state["client_id_counter"] += 1
    client_id = app_state["client_id_counter"]
    connection = {"websocket": websocket, "client_id": client_id}
    app_state["active_connections"].append(connection)

    # Send client their ID
    await websocket.send_text(json.dumps({"type": "connected", "client_id": client_id}))

    # Send message history to the new client
    for msg in app_state["message_history"]:
        await websocket.send_text(json.dumps(msg))

    try:
        while True:
            data = await websocket.receive_text()
            message = {"sender": client_id, "message": data}
            app_state["message_history"].append(message)  # Store the message
            await broadcast(json.dumps(message))  # Broadcast to all
    except WebSocketDisconnect:
        app_state["active_connections"].remove(connection)
        print(f"Client {client_id} disconnected")