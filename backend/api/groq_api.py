from groq import Groq
from backend.config import Config

class GroqClient:
    def __init__(self):
        self.groq_client = Groq(api_key=Config.GROQ_API_KEY)

    def get_groq_client(self):
        return self.groq_client