import streamlit as st
import json
from json import JSONDecodeError
from backend.config import Config
from backend.utils import remove_code_markers

class Research:
    def __init__(self, query, context_data, summarizer_agent, reviewer_agent, reference_links):
        self.query = query
        self.context_data = context_data
        self.summarizer_agent = summarizer_agent
        self.reviewer_agent = reviewer_agent
        self.reference_links = reference_links
        self.iteration_data = []  # To store iteration results

    def conduct_research(self, max_iterations=Config.MAX_ITERATIONS):
        best_response = None
        highest_score = 0
        feedback = None  # No feedback for the first iteration

        for iteration in range(1, max_iterations + 1):
            # Step 1: Summarize the context, optionally using feedback
            if feedback:
                response = self.summarizer_agent.get_summary(self.query, self.context_data, feedback, self.reference_links)
            else:
                response = self.summarizer_agent.get_summary(self.query, self.context_data, "None", self.reference_links)
            
            st.markdown(f"""
                <div class="chat-box">
                    <span class="icon">✍️</span>
                    <span class="summarizer-role">Summarizer: </span>
                    Summarization for trial {iteration} completed. <span class="bold-text">Waiting for Reviewer Response.</span>
                </div>""", unsafe_allow_html=True)

            print(f"Summary {iteration}: {response}")

            # Step 2: Review the response
            review_response = self.reviewer_agent.get_review(self.query, self.context_data, response)
            review_response_cleaned = remove_code_markers(review_response)

            try:
                review = json.loads(review_response_cleaned)
            except JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                review = {
                    "status": "NOT ACCEPTED",
                    "feedback": "Error parsing JSON response from reviewer agent.",
                    "ACCEPTANCE_SCORE": 0,
                }

            st.markdown(f"""
                <div class="chat-box">
                    <span class="icon">🧐</span>
                    <span class="reviewer-role">Reviewer: </span>
                    <span class="bold-text">Review Feedback for trail {iteration}:</span> {review['feedback']}
                    <div class="score">Acceptance Score for trail {iteration}: {review['ACCEPTANCE_SCORE']}%</div>
                </div>""", unsafe_allow_html=True)

            if review["status"] == "NOT ACCEPTED" and iteration != 3:
                st.markdown(f"""
                    <div class="chat-box">
                        <span class="icon">✍️</span>
                        <span class="reviewer-role">Summarizer: </span>
                        Thanks for the feedback. <span class="bold-text">Trying to do better...</span>
                    </div>""", unsafe_allow_html=True)
                
            # Step 3: Store iteration data
            self.iteration_data.append({
                "iteration": iteration,
                "response": response,
                "feedback": review.get("feedback", "No feedback provided."),
                "score": review.get("ACCEPTANCE_SCORE", 0),
            })

            # print(f"Iteration: {iteration}\nReviewer Response: {review}")

            # Check if status is ACCEPTED
            if review["status"] == "ACCEPTED":
                best_response = response
                break

            # Update feedback for the next iteration
            feedback = review["feedback"]

            # Update best response if the current score is higher
            if review["ACCEPTANCE_SCORE"] > highest_score:
                highest_score = review["ACCEPTANCE_SCORE"]
                best_response = response

        # Append reference links to the final response
        final_output = f"{best_response}"

        return {
            "final_output": final_output,
            "iterations": self.iteration_data,
        }
