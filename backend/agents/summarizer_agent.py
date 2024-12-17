from backend.api.groq_api import GroqClient
from backend.config import Config

class SummarizerAgent:
    def __init__(self):
        groq_instance = GroqClient()
        self.query_enhancer = groq_instance.get_groq_client()
    
    def prompt_template(self, query, context, feedback, reference_links):
        prompt = f"""
You are a highly skilled Research Member in an R&D team responsible for producing comprehensive, professional, and insightful research reports. Your task is to generate a detailed research report based on the provided user query, context, and reference links. Your output should be structured, logical, and tailored for academic or professional use.

### Guidelines:
1. **User Query as Focus**: The user query represents the primary topic of the research. Align the report to this query.
2. **Contextual Analysis**: Utilize the provided context to extract and analyze relevant information.
3. **Incorporate Feedback**: If feedback is provided, use it to refine and enhance the research report.
4. **Professional Structure**:
    - **Title**: Provide a clear, concise title that encapsulates the essence of the report.
    - **Introduction**: Provide a brief overview of the topic and the report's objective.
    - **Key Insights**: Highlight the most important findings related to the topic.
    - **Comparative Analysis**: Include comparisons with similar models, products, or relevant benchmarks.
    - **Strategic Recommendations**: Offer actionable suggestions or implications for the topic.
    - **Conclusion**: Summarize the key takeaways and provide a forward-looking perspective.
5. **Enrich the Content**:
    - Include examples, comparisons, and relevant statistics to support your analysis.
    - Use formal language and avoid redundancy or unnecessary details.
6. **Reference Links**:
    - Add a "Reference Links" section at the end of the report, listing all provided links as bullet points.
7. **Word Limit**: The research report should be detailed and fall within 500-600 words.
8. **Markdown Compatible**: Ensure the report is written in Markdown format for easy readability and formatting.

### Input:
User Query (Topic): {query}
Context: {context}
Reference Links: {reference_links}
Feedback (if any): {feedback}

### Output:
Provide a structured, professional research report with the following sections (BUT NOT LIMITED TO THIS):
1. **Introduction**
2. **Key Insights**
3. **Comparative Analysis**
4. **Strategic Recommendations**
5. **Conclusion**
6. **Reference Links**
"""
        return prompt
    
    def get_summary(self, user_query, context, feedback, reference_links):
        chat_completion = self.query_enhancer.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": self.prompt_template(user_query, context, feedback, reference_links),
                }
            ],
            model=Config.GROQ_MODEL_NAME,
            max_tokens=Config.GROQ_MAX_TOKENS,
        )

        response = chat_completion.choices[0].message.content

        return response