import os
import pinecone
from typing import List
from openai import OpenAI

class VectorStore:
    def __init__(self):
        # Initialize Pinecone
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
        self.index_name = "knowthee-index"
        # Create index if it doesn't exist
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(self.index_name, dimension=1536, metric="cosine")
        self.index = pinecone.Index(self.index_name)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_text(self, texts: List[str]) -> List[List[float]]:
        # Use OpenAI to embed text (1536-dim for text-embedding-ada-002)
        response = self.client.embeddings.create(
            input=texts,
            model="text-embedding-ada-002"
        )
        return [d.embedding for d in response.data]

    def store_documents(self, documents: List[str]):
        # Remove all vectors from the index (for demo simplicity)
        # Pinecone doesn't have a 'delete all', so fetch and delete by ID
        existing_ids = [m["id"] for m in self.index.describe_index_stats()["namespaces"].get("", {}).get("vectors", [])]
        if existing_ids:
            self.index.delete(ids=existing_ids)
        # Add new documents
        embeddings = self.embed_text(documents)
        ids = [f"doc-{i}" for i in range(len(documents))]
        to_upsert = list(zip(ids, embeddings, documents))
        self.index.upsert(vectors=[(id, vec, {"text": doc}) for id, vec, doc in to_upsert])

    def get_relevant_chunks(self, query: str = None, n_results: int = 5) -> List[str]:
        # If no query, return all documents (not efficient for large sets)
        if not query:
            stats = self.index.describe_index_stats()
            all_ids = [m["id"] for m in stats["namespaces"].get("", {}).get("vectors", [])]
            if not all_ids:
                return []
            results = self.index.fetch(ids=all_ids)
            return [v["metadata"]["text"] for v in results["vectors"].values()]
        # Embed the query and search
        query_vec = self.embed_text([query])[0]
        results = self.index.query(vector=query_vec, top_k=n_results, include_metadata=True)
        return [match.metadata["text"] for match in results.matches]

    def clear(self):
        # Remove all vectors from the index
        existing_ids = [m["id"] for m in self.index.describe_index_stats()["namespaces"].get("", {}).get("vectors", [])]
        if existing_ids:
            self.index.delete(ids=existing_ids) 