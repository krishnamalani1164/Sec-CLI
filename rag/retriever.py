from rag.local_store import LocalVectorStore

class RAGRetriever:
    def __init__(self, k=3):
        self.store = LocalVectorStore()
        self.k = k

    def retrieve(self, query: str):
        return self.store.search(query, k=self.k)
