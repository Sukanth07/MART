from backend.config import Config

class VectorRetriever:
    def __init__(self):
        pass

    def retrieve_similar_documents(self, query, vector_store):
        results = vector_store.similarity_search(query, k=Config.TOP_K)
        return results