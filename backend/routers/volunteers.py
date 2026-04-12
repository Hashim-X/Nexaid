from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.firebase_service import add_document, get_documents
from datetime import datetime

router = APIRouter()

class VolunteerRegistration(BaseModel):
    name: str
    skills: List[str]
    location: str
    availability: bool = True

@router.post("/register")
async def register_volunteer(volunteer: VolunteerRegistration):
    try:
        vol_dict = volunteer.model_dump()
    except AttributeError:
        vol_dict = volunteer.dict()  # Fallback for Pydantic v1
        
    vol_dict["created_at"] = datetime.utcnow().isoformat()
    doc_id = add_document("volunteers", vol_dict)
    vol_dict["id"] = doc_id
    return {"volunteer": vol_dict}

@router.get("")
async def get_volunteers():
    volunteers = get_documents("volunteers")
    return {"volunteers": volunteers}
