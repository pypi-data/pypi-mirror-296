from typing import List, Optional
from unittest.mock import MagicMock, AsyncMock

class MockOpenAIEmbeddings:
    def __init__(self, embedding_size: int):
        """
        Initialize the mock OpenAIEmbeddings with a specified embedding size.
        """
        self.embedding_size = embedding_size
        self._get_len_safe_embeddings = MagicMock()
        self._aget_len_safe_embeddings = AsyncMock()  # Use AsyncMock for async methods
        self.deployment = "mock_deployment"

    def embed_query(self, text: str) -> List[float]:
        """
        Mock embedding query method.
        """
        embeddings = self._get_len_safe_embeddings([text], engine=self.deployment)
        return embeddings[0]

    async def aembed_query(self, text: str) -> List[float]:
        """
        Mock async embedding query method.
        """
        embeddings = await self._aget_len_safe_embeddings([text], engine=self.deployment)
        return embeddings[0]

    def embed_documents(
            self, texts: List[str], chunk_size: Optional[int] = 0
    ) -> List[List[float]]:
        """
        Mock embedding documents method.
        """
        return self._get_len_safe_embeddings(texts, engine=self.deployment)

    async def aembed_documents(
            self, texts: List[str], chunk_size: Optional[int] = 0
    ) -> List[List[float]]:
        """
        Mock async embedding documents method.
        """
        return await self._aget_len_safe_embeddings(texts, engine=self.deployment)

    def set_embeddings(self, embeddings: List[List[float]]):
        """
        Set the mock return value for `_get_len_safe_embeddings`.
        """
        self._get_len_safe_embeddings.return_value = embeddings

    async def set_aembeddings(self, embeddings: List[List[float]]):
        """
        Set the mock return value for `_aget_len_safe_embeddings`.
        """
        self._aget_len_safe_embeddings.return_value = embeddings
