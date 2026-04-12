from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.firebase_service import add_document, get_documents, update_document
from services.gemini_service import extract_needs, get_dashboard_summary
from datetime import datetime

router = APIRouter()

class NeedSubmission(BaseModel):
    raw_text: str
    location: str

@router.post("/submit")
async def submit_need(submission: NeedSubmission):
    try:
        extracted = extract_needs(submission.raw_text, submission.location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    saved_needs = []
    if not extracted:
        return {"needs": []}
    
    for need in extracted:
        # Add extra fields
        need_data = need.copy()
        need_data["status"] = "active"
        need_data["location"] = submission.location
        need_data["raw_text"] = submission.raw_text
        need_data["created_at"] = datetime.utcnow().isoformat()
        
        need_id = add_document("needs", need_data)
        need_data["id"] = need_id
        saved_needs.append(need_data)
        
    return {"needs": saved_needs}

@router.get("/active")
async def get_active_needs():
    needs = get_documents("needs", filters=[("status", "==", "active")])
    if not needs:
        return {"needs": [], "summary": None}
    
    summary = get_dashboard_summary(needs)
    return {"needs": needs, "summary": summary}
