from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from scripts import get_data


router = APIRouter()


class PropertiesData(BaseModel):
    wiki_url: str
    sparql_endpoint: str

connections = {}

async def process_classes_data(request_id: str, websocket: WebSocket):
    classes_data = get_data.get_classes(request_id)
    await websocket.send_json({"status": "done", "request_id": request_id, "data": classes_data})
    await websocket.close()

async def process_properties_data(request_id: str, sparql_endpoint: str, wiki_url: str, websocket: WebSocket):
    properties_data, connected_properties, edges, nodes = get_data.get_properties(sparql_endpoint, wiki_url)
    data = {"properties": properties_data, "connected": connected_properties, "edges": edges, "nodes": nodes}
    await websocket.send_json({"status": "done", "request_id": request_id, "data": data})
    await websocket.close()


@router.websocket("/ws/classes/{request_id}")
async def websocket_endpoint_classes(request_id: str, websocket: WebSocket):
    await websocket.accept()
    connections[request_id] = websocket
    try:
        await process_classes_data(request_id, websocket)
    except WebSocketDisconnect:
        print(f"Client {request_id} disconnected")
        del connections[request_id]

@router.websocket("/ws/properties/{request_id}")
async def websocket_endpoint_properties(request_id: str, websocket: WebSocket):
    await websocket.accept()
    connections[request_id] = websocket
    try:
        initial_data = await websocket.receive_text()
        instance_info = PropertiesData.parse_raw(initial_data)
        wiki_url = instance_info.wiki_url
        sparql_endpoint = instance_info.sparql_endpoint
        await process_properties_data(request_id, sparql_endpoint, wiki_url, websocket)
    except WebSocketDisconnect:
        print(f"Client {request_id} disconnected")
        del connections[request_id]


