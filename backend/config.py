import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    # Basic Configurations
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = Path(os.path.dirname(curr_dir))

    # Serper API Configurations
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    SERPER_URL = "https://google.serper.dev/search"
    SERPER_COUNTRY = "in"
    SERPER_NUM_RESULTS = 10
    
    # Groq API Configurations
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL_NAME = "llama-3.3-70b-versatile"
    GROQ_MAX_TOKENS = 2048

    # Vector Store Configurations
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_EMBEDDING_MODEL = "models/embedding-001"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP_SIZE = 150
    TOP_K = 3
    
    # Research Configurations
    MAX_ITERATIONS = 3