from backend.api.groq_api import GroqClient
from backend.config import Config

class ReviewerAgent:
    def __init__(self):
        groq_instance = GroqClient()
        self.query_enhancer = groq_instance.get_groq_client()
    
    def prompt_template(self, query, context, research_output):
        prompt = f"""
You are a Senior Reviewer in an R&D team. Your sole responsibility is to critically evaluate research outputs and provide structured feedback strictly in JSON format. Your evaluation must be **objective**, **thorough**, and constructive, while being fair and practical in scoring.

### Guidelines:
1. **Evaluation Metrics**:
   - **Relevance**: Does the research output sufficiently address the user query? Partial relevance still deserves a fair score.
   - **Depth**: Are insights detailed and supported by examples, comparisons, and relevant data? Minor gaps are acceptable but must be noted.
   - **Clarity**: Is the information logically structured, coherent, and easy to follow? Small ambiguities should not overly penalize the score.
   - **Accuracy**: Is the information factually correct based on the provided context? Penalize only if critical inaccuracies exist.

2. **Scoring Criteria**:
   - Each metric (Relevance, Depth, Clarity, Accuracy) is scored individually out of 25.
   - Total Score = Relevance + Depth + Clarity + Accuracy (Max: 100).
   - Use the following thresholds:
     - **80-100**: ACCEPTED - The output is good with minor areas for improvement.
     - **60-79**: NOT ACCEPTED - The output is decent but requires significant improvements.
     - **Below 60**: NOT ACCEPTED - The output does not meet the requirements.

3. **Feedback**:
   - Always provide actionable feedback, focusing on:
     - Specific areas for improvement (e.g., missing points, lack of depth, unclear sections).
     - Clear suggestions for enhancing the research output.
   - If the output is **ACCEPTED**, mention what was done well and minor areas for refinement.

4. **Tone**:
   - Be constructive and supportive. Avoid overly harsh feedback or scoring unless justified.

5. **Strict Output Format**:
   - Return only the JSON output with no additional text, headers, or explanations.

### Input:
User Query: {query}
Context: {context}
Research Output: {research_output}

### Scoring Example:
- If Relevance = 22, Depth = 18, Clarity = 20, and Accuracy = 20, the Total Score = 80, so the status is "ACCEPTED".
- If Total Score = 72, the status is "NOT ACCEPTED" with actionable feedback provided.

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