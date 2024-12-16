from backend.api.groq_api import GroqClient
from backend.config import Config

class QueryEnhancer:
    def __init__(self):
        groq_instance = GroqClient()
        self.query_enhancer = groq_instance.get_groq_client()

    def prompt_template(self, user_query):
        prompt = f"""
You are an intelligent Query Enhancement Agent.
Instruction: Your task is to enhance user queries for search engines by making them concise, optimized, and precise while retaining their intent. The enhanced query must be short (5 to 8 words) and include:
1. Synonyms or alternate terms for key words.
2. Relevant keywords or phrases that broaden the search scope while staying concise.

Guidelines:
1. Analyze the user's query and identify key terms.
2. Replace key terms with synonyms or related words if necessary.
3. Add 1-2 additional relevant keywords, ensuring the query remains concise.
4. Do not return more than 5 to 8 words.
5. Only return the enhanced query without any additional explanation or formatting.

User Query: "{user_query}"
"""
        return prompt
    
    def get_enhanced_query(self, user_query):
        chat_completion = self.query_enhancer.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": self.prompt_template(user_query),
                }
            ],
            model=Config.GROQ_MODEL_NAME,
        )

        response = chat_completion.choices[0].message.content

        cleaned_response = response.strip('"\'')
        
        return cleaned_response