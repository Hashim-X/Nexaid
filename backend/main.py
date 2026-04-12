import os
from dotenv import load_dotenv

# Load .env at the very top
load_dotenv()

import firebase_admin
from firebase_admin import credentials

# Initialize Firebase before routers are imported
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers after Firebase initialization
from routers import needs, volunteers, matches

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(needs.router, prefix="/api/needs", tags=["needs"])
app.include_router(volunteers.router, prefix="/api/volunteers", tags=["volunteers"])
app.include_router(matches.router, prefix="/api/matches", tags=["matches"])

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "firebase": "connected",
        "gemini": "configured"
    }
