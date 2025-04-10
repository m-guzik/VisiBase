from fastapi import BackgroundTasks, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import time

from scripts import get_data

app = FastAPI() 


app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
connections = {}



@app.get("/")
def home():
    return {"message": "Welcome to VisiBase API!"}



async def process_data(request_id: str, websocket: WebSocket):
    classes_data = get_data.get_classes(request_id)
    await websocket.send_json({"status": "done", "request_id": request_id, "data": classes_data})
    await websocket.close()


async def process_properties_data(request_id: str, websocket: WebSocket):
    properties_data, connected_properties = get_data.get_properties(request_id)
    data = {"properties": properties_data, "connected": connected_properties}
    await websocket.send_json({"status": "done", "request_id": request_id, "data": data})
    await websocket.close()


@app.websocket("/ws/{request_id}")
async def websocket_endpoint(request_id: str, websocket: WebSocket):
    await websocket.accept()
    connections[request_id] = websocket
    try:
        await process_data(request_id, websocket)
    except WebSocketDisconnect:
        print(f"Client {request_id} disconnected")
        del connections[request_id]

@app.websocket("/pws/{request_id}")
async def websocket_endpoint(request_id: str, websocket: WebSocket):
    await websocket.accept()
    connections[request_id] = websocket
    try:
        await process_properties_data(request_id, websocket)
    except WebSocketDisconnect:
        print(f"Client {request_id} disconnected")
        del connections[request_id]

