import streamlit as st
from backend.workflow_manager import WorkflowManager

st.set_page_config(
    page_title="MART",
    page_icon=":robot_face:",
)

# Custom CSS for styling
st.markdown("""
    <style>
        .final-output-heading {
            font-size: 2em;
            font-weight: bold;
            color: #e8eded;
            margin-top: 20px;
            margin-bottom: 8px;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("Multi Agents Research Team 🤖")

    # User input
    user_query = st.chat_input(placeholder="Research about something...")
    
    if user_query:
        workflow = WorkflowManager(user_query=user_query)
        final_output, iterations = workflow.process_workflow()

        # Display Final Output

        st.markdown(
            """
            <div class="final-output-heading">Final Research Output:</div>
            <hr>
            """, unsafe_allow_html=True
        )

        st.markdown(
            f"""
            {final_output}
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
