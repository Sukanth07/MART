"""
1. Get user_query from Input in app.py
2. Get enhanced link using agent->link_enhancer.py
3. Pass the enhanced link to tools->links_collector.py
4. Pass the collected organic links to tools->webscraper.py
5. Pass the scraped data to tools->vector_store.py
6. Pass the vector data to tools->vector_retriever.py
7. Pass the retrieved context to tools->research.py
8. Loop upto three times to get the final answer using agents -> summarizer_agent.py and reviewer_agent.py
9. Add the reference links in the end of final answer
10. Return the final answer to app.py
"""
import streamlit as st
from backend.utils import styles
from backend.agents.query_enhancer import QueryEnhancer
from backend.tools.links_collector import LinksCollector
from backend.tools.webscraper import WebScraper
from backend.tools.vector_store import VectorStore
from backend.tools.vector_retriever import VectorRetriever
from backend.tools.research import Research
from backend.agents.summarizer_agent import SummarizerAgent
from backend.agents.reviewer_agent import ReviewerAgent

class WorkflowManager:
    def __init__(self, user_query):
        self.user_query = user_query
        self.query_enhancer = QueryEnhancer()
        self.links_collector = LinksCollector()
        self.web_scraper = WebScraper()
        self.vector_store = VectorStore()
        self.vector_retriever = VectorRetriever()
        self.summarizer_agent = SummarizerAgent()
        self.reviewer_agent = ReviewerAgent()

    def process_workflow(self):
        
        markdown_css = styles()

        # 1. Get enhanced link
        enhanced_query = self.query_enhancer.get_enhanced_query(user_query=self.user_query)

        print("\nENHANCED QUERY:", enhanced_query)
        st.markdown(f"""
            <div class="chat-box">
                <span class="icon">💡</span>
                <span class="query-role">Query Enhancer: </span>
                Original query enhanced to <span class="bold-text">{enhanced_query}</span>
            </div>""", unsafe_allow_html=True)

        # 2. Collect the Organic Links
        organic_links = self.links_collector.get_organic_links(query=enhanced_query)

        print("\nORGANIC LINKS: ", organic_links)
        st.markdown(f"""
            <div class="chat-box">
                <span class="icon">🔍</span>
                <span class="url-role">URLs Collector: </span>
                URLs collected successfully.
            </div>""", unsafe_allow_html=True)

        # 3. Get the Web Scraped Data
        scraped_data = self.web_scraper.scrape(urls=organic_links)

        print("\nData Scraped Successfully..")
        st.markdown(f"""
            <div class="chat-box">
                <span class="icon">🕸️</span>
                <span class="scraper-role">Web Scraper: </span>
                Scraped content from collected URLs successfully.
            </div>""", unsafe_allow_html=True)
        
        # 4. Pass the scraped data to vector store
        vector_store = self.vector_store.store_data(data=scraped_data)

        print("\nStored the data in Vector Store..")

        # 5. Pass the vector data to vector retriever
        retrieved_data = self.vector_retriever.retrieve_similar_documents(query=self.user_query, vector_store=vector_store)

        print("\nRetrieved the similar documents..")

        # 6. Conduct research on the retrieved data
        self.research_agents = Research(
            query=enhanced_query,
            context_data=retrieved_data,
            summarizer_agent=self.summarizer_agent,
            reviewer_agent=self.reviewer_agent,
            reference_links=organic_links
        )

        research_response = self.research_agents.conduct_research()

        print("\nResearch Completed...")

        # 7. Extract and return results
        final_output = research_response["final_output"]
        iterations = research_response["iterations"]

        return final_output, iterations
