from backend.api.groq_api import GroqClient
from backend.config import Config
from datetime import datetime

class QueryEnhancer:
    def __init__(self):
        groq_instance = GroqClient()
        self.query_enhancer = groq_instance.get_groq_client()

    def prompt_template(self, user_query):
        year = datetime.now().year
        prompt = f"""
You are a Search Query Enhancement Agent responsible for improving user queries to make them highly specific, clear, and optimized for search engines. Your enhancements should **preserve the original intent**, make the query **more focused**, and **improve its relevance** without making it overly broad or ambiguous.

### Guidelines:
1. **Preserve Intent**:
   - Ensure the original query's focus is maintained. Do not change its meaning or purpose.

2. **Add Specificity**:
   - Add relevant details like "{year}", "latest," "top," or clarifiers like "cost-effective," "best-performing," or "open-source," where applicable.
   - Example: If the query is vague like "cloud storage," enhance it to "best affordable cloud storage solutions "{year}"."

3. **Enhance Clarity**:
   - Rephrase queries to be more direct, readable, and well-formed for search engines.
   - Correct any grammatical errors or ambiguities in the input query.

4. **Make It Contextually Relevant**:
   - Use contextually appropriate keywords or phrases based on the query type.
   - For general queries: Add trending or relevant keywords.
   - For research-oriented queries: Add specificity like "in-depth analysis" or "case studies."
   - For comparison queries: Add phrases like "alternatives," "comparisons," or "reviews."

5. **Be Concise**:
   - Keep the enhanced query short and to the point (5-8 words max).

6. **Generic Behavior**:
   - The enhancement must suit **any type of query**: whether it's about products, research, comparisons, tools, or generic search topics.

### Input Query:
{user_query}

### Output:
Return only the enhanced query in one line, with no additional explanation, text, or formatting.
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