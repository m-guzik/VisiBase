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
    wiki_data = get_data.get_classes(request_id)
    data = {"message": request_id, "data": wiki_data}
    await websocket.send_json({"status": "done", "data": data})
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
