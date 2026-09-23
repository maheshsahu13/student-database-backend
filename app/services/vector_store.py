import chromadb

from app.services.embedding_service import EmbeddingService


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")

        self.collection = self.client.get_or_create_collection(
            name="students"
        )

        self.embedding_service = EmbeddingService()

    def add_student(
        self,
        student_id: int,
        text: str,
        metadata: dict,
    ):
        embedding = self.embedding_service.create_embedding(text)

        self.collection.upsert(
            ids=[str(student_id)],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
        )

    def search(self, query: str, n_results: int = 5):
        query_embedding = self.embedding_service.create_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )

        return results