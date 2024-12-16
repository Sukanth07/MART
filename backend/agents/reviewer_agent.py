from backend.api.groq_api import GroqClient
from backend.config import Config

class ReviewerAgent:
    def __init__(self):
        groq_instance = GroqClient()
        self.query_enhancer = groq_instance.get_groq_client()
    
    def prompt_template(self, query, context, research_output):
        prompt = f"""
    You are a Senior Reviewer in an R&D team. Your sole responsibility is to critically evaluate research outputs and provide structured feedback strictly in JSON format. Your evaluation must be **objective**, **thorough**, and follow specific scoring criteria.

    ### Guidelines:
    1. Evaluate the research output based on the following metrics:
    - **Relevance**: Does it fully and accurately address the user query? If any part of the query is missing or incomplete, deduct points.
    - **Depth**: Does the research provide thorough insights, examples, comparisons, and statistics? Superficial or shallow content must result in a deduction.
    - **Clarity**: Is the content logically structured, easy to follow, and free of contradictions or ambiguities?
    - **Accuracy**: Validate the correctness of the information presented based on the provided context.
    2. **Scoring Criteria**:
    - Score each metric (Relevance, Depth, Clarity, and Accuracy) individually out of 25.
    - Total Score = Relevance + Depth + Clarity + Accuracy (Max: 100).
    - If the **Total Score < 80**, the status must be "NOT ACCEPTED".
    3. Provide actionable feedback for improvement, focusing on:
    - Missing points or gaps in the research.
    - Suggestions for adding more depth, accuracy, or clarity.
    4. **Strict Output Format**:
    - Return only the JSON output with no additional text, headers, or explanations.

    ### Input:
    User Query: {query}
    Context: {context}
    Research Output: {research_output}

    ### Scoring Example:
    If Relevance = 20, Depth = 15, Clarity = 18, and Accuracy = 22, the Total Score = 75, so the status must be "NOT ACCEPTED".

    ### Output:
    Return a JSON object strictly in this format:
    {{
        "status": "ACCEPTED" or "NOT ACCEPTED",
        "feedback": "<Provide specific feedback on what needs to be improved or why it was accepted>",
        "ACCEPTANCE_SCORE": <Total numerical score out of 100>
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