from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class InstanceData(BaseModel):
    name: str
    api_address: str
    sparql_endpoint: str

@router.post("/api/submitInstanceInfo")
async def submit_instance(data: InstanceData):
    print("Received data:", data)
    
    return {"message": f"Received instance {data.name}"}

