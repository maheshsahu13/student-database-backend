from app.services.vector_store import VectorStore


class RetrievalService:
    def __init__(self):
        self.vector_store = VectorStore()

    def semantic_search(
        self,
        query: str,
        n_results: int = 5,
    ):
        results = self.vector_store.search(
            query=query,
            n_results=n_results,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved_students = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            retrieved_students.append(
                {
                    "document": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        return retrieved_students