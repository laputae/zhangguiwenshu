from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance

from app.conf.app_config import app_config


class ColumnQdrantRepository:
    collection_name = "column_info_collection"

    def __init__(self, client: AsyncQdrantClient):
        self.client = client

    async def ensure_collection(self):
        if not await self.client.collection_exists(collection_name=self.collection_name):
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=app_config.qdrant.embedding_size, distance=Distance.COSINE)
            )
