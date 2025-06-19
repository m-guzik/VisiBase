from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from scripts import get_data


router = APIRouter()


class ClassesData(BaseModel):
    wiki_url: str
    sparql_endpoint: str
    api_endpoint: str

class PropertiesData(BaseModel):
    wiki_url: str
    sparql_endpoint: str

connections = {}

async def process_classes_data(request_id: str, websocket: WebSocket, sparql_endpoint: str, wiki_url: str, api_endpoint:str):
    classes_data, edges, nodes, edge_labels = get_data.get_classes(sparql_endpoint, wiki_url, api_endpoint)
    data = {"classes": classes_data, "edges": edges, "nodes": nodes, "labels": edge_labels}
    await websocket.send_json({"status": "done", "request_id": request_id, "data": data})
    await websocket.close()

async def process_properties_data(request_id: str, websocket: WebSocket, sparql_endpoint: str, wiki_url: str):
    properties_data, connected_properties, edges, nodes, edges_labels = get_data.get_properties(sparql_endpoint, wiki_url)
    data = {"properties": properties_data, "connected": connected_properties, "edges": edges, "nodes": nodes, "labels": edges_labels}
    await websocket.send_json({"status": "done", "request_id": request_id, "data": data})
    await websocket.close()


@router.websocket("/ws/classes/{request_id}")
async def websocket_endpoint_classes(request_id: str, websocket: WebSocket):
    await websocket.accept()
    connections[request_id] = websocket
    try:
        initial_data = await websocket.receive_text()
        instance_info = ClassesData.parse_raw(initial_data)
        wiki_url = instance_info.wiki_url
        sparql_endpoint = instance_info.sparql_endpoint
        api_endpoint = instance_info.api_endpoint
        await process_classes_data(request_id, websocket, sparql_endpoint, wiki_url, api_endpoint)
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
        await process_properties_data(request_id, websocket, sparql_endpoint, wiki_url)
    except WebSocketDisconnect:
        print(f"Client {request_id} disconnected")
        del connections[request_id]


