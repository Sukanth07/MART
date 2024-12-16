import streamlit as st

def remove_code_markers(response):
    markers = ["```json", "```"]

    # Check if the response starts and ends with any of the markers
    for marker in markers:
        if response.startswith(marker):
            response = response[len(marker):].lstrip()  # Remove the marker and leading whitespace
        if response.endswith(marker):
            response = response[:-len(marker)].rstrip()  # Remove the marker and trailing whitespace
    
    # Check if the response contains any of the markers
    if "```" in response:
        response = response.replace("```", '')

    # Check if the response contains any of the markers with language names
    marker_names = ["json"]
    for marker in marker_names:
        if f"```{marker}" in response:
            response = response.replace(f"```{marker}", '')

    return response

def styles():
    markdown_style = st.markdown(
    """
        <style>
        .chat-box {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px 15px;
            margin: 10px 0px;
            background-color: #171626;
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
        }
        .bold-text {
            font-weight: bold;
            color: #fff;
        }
        .score {
            font-size: 1.1em;
            color: #4CAF50;
            font-weight: bolder;
            margin-top: 10px;
        }
        .icon {
            font-size: 1.2em;
            margin-right: 5px;
        }
        .query-role{
            font-weight: bold;
            color: #b30086;
        }
        .url-role{
            font-weight: bold;
            color: #00a3cc;
        }
        .scraper-role{
            font-weight: bold;
            color: #cc5200;
        }
        .summarizer-role{
            font-weight: bold;
            color: #008000;
        }
        .reviewer-role{
            font-weight: bold;
            color: #cc9900;
        }
        </style>
    """, unsafe_allow_html=True)
    
    return markdown_style