from rag.local_store import LocalVectorStore

if __name__ == "__main__":
    store = LocalVectorStore()
    store.build()