from fastapi import APIRouter, HTTPException
from services.firebase_service import get_documents, add_document, update_document
from services.gemini_service import match_volunteer
from datetime import datetime

router = APIRouter()

@router.post("/{need_id}")
async def create_match(need_id: str):
    # Fetch need by id from needs collection
    all_needs = get_documents("needs")
    need = next((n for n in all_needs if n.get("id") == need_id), None)
    
    if not need:
        raise HTTPException(status_code=404, detail="Need not found")
        
    # Fetch all volunteers
    volunteers = get_documents("volunteers")
    if not volunteers:
        raise HTTPException(status_code=400, detail="No volunteers registered yet")
        
    # Match using Gemini
    match_result = match_volunteer(need, volunteers)
    
    volunteer_id = match_result.get("volunteer_id")
    
    # Save to matches collection
    match_data = {
        "need_id": need_id,
        "volunteer_id": volunteer_id,
        "match_reason": match_result.get("reason"),
        "confidence_score": match_result.get("match_score"),
        "urgency_flag": match_result.get("urgency_flag", False),
        "created_at": datetime.utcnow().isoformat()
    }
    
    add_document("matches", match_data)
    
    # Update need status
    update_document("needs", need_id, {"status": "matched"})
    
    # Fetch matched volunteer details
    volunteer = next((v for v in volunteers if v.get("id") == volunteer_id), None)
    
    return {"match": match_data, "volunteer": volunteer}
