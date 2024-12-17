from backend.api.groq_api import GroqClient
from backend.config import Config

class ReviewerAgent:
    def __init__(self):
        groq_instance = GroqClient()
        self.query_enhancer = groq_instance.get_groq_client()
    
    def prompt_template(self, query, context, research_output):
        prompt = f"""
You are a Senior Reviewer in an R&D team. Evaluate the research output fairly and provide structured feedback in JSON format.

### Constraints:
- Provide the response strictly in json format.
- Don't give any additional information or explainations beyond the json formatted output.
- The Keys in json output are case sensitive. So ensure you provide proper json response.

### Evaluation Metrics:
1. **Relevance**: Does it address the user query?
2. **Depth**: Are there sufficient details, examples, or comparisons?
3. **Clarity**: Is the content well-structured and easy to understand?
4. **Accuracy**: Is the information correct based on the context?

### Scoring:
- Each metric is scored out of 25 (Max: 100).
- Status thresholds:
   - **80-100**: ACCEPTED (Good with minor refinements).
   - **Below 80**: NOT ACCEPTED (Needs improvement).

### Feedback:
- Provide actionable and brief suggestions for improvement.
- If **ACCEPTED**, highlight strengths and minor areas for refinement.

### Input:
User Query: {query}
Context: {context}
Research Output: {research_output}

### Output Format:
{{
    "status": "ACCEPTED" or "NOT ACCEPTED",
    "feedback": "<Brief feedback on areas for improvement or strengths>",
    "ACCEPTANCE_SCORE": <Total score out of 100>
}}
"""

        return prompt

    
    def get_review(self, user_query, context, research_output):
        chat_completion = self.query_enhancer.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": self.prompt_template(user_query, context, research_output),
                }
            ],
            model=Config.GROQ_MODEL_NAME,
            max_tokens=Config.GROQ_MAX_TOKENS,
        )

        response = chat_completion.choices[0].message.content

        return response