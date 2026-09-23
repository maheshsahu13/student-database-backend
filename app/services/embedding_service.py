import os
from google import genai


class EmbeddingService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-embedding-001"

    def create_embedding(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
        )

        return response.embeddings[0].values