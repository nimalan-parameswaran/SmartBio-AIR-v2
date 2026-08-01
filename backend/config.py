import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    FIREBASE_DATABASE_URL = os.getenv(
        "FIREBASE_DATABASE_URL", 
        "https://smartbioair-v1-default-rtdb.asia-southeast1.firebasedatabase.app"
    )
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "smartbioair-v1")
    PORT = int(os.getenv("PORT", "8000"))
    HOST = os.getenv("HOST", "0.0.0.0")
    
    # Mode selection: 'firebase' or 'local'
    # Automatically defaults to 'firebase' if database URL is reachable/valid, or falls back to 'local' if needed.
    DATABASE_MODE = os.getenv("DATABASE_MODE", "firebase")
    
    # Path to local database file (for local fallback mode)
    LOCAL_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "local_db.json"))
