from typing import Annotated

from fastapi import Depends
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.repositories.es.value_es_repository import ValueESRepository
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository
from app.services.query_service import QueryService


async def get_embedding_client() -> HuggingFaceEndpointEmbeddings:
    pass


async def get_value_es_repository() -> ValueESRepository:
    pass


async def get_meta_mysql_repository() -> MetaMySQLRepository:
    pass


async def get_column_qdrant_repository() -> ColumnQdrantRepository:
    pass


async def get_metric_qdrant_repository() -> MetricQdrantRepository:
    pass


async def get_dw_mysql_repository() -> DWMySQLRepository:
    pass


async def get_query_service(embedding_client: Annotated[HuggingFaceEndpointEmbeddings, Depends(get_embedding_client)],
                            dw_mysql_repository: Annotated[DWMySQLRepository, Depends(get_dw_mysql_repository)],
                            metric_qdrant_repository: Annotated[
                                MetricQdrantRepository, Depends(get_metric_qdrant_repository)],
                            value_es_repository: Annotated[ValueESRepository, Depends(get_value_es_repository)],
                            column_qdrant_repository: Annotated[
                                ColumnQdrantRepository, Depends(get_column_qdrant_repository)],
                            meta_mysql_repository: Annotated[MetaMySQLRepository, Depends(get_meta_mysql_repository)]
                            ) -> QueryService:
    return QueryService(meta_mysql_repository=meta_mysql_repository,
                        dw_mysql_repository=dw_mysql_repository,
                        metric_qdrant_repository=metric_qdrant_repository,
                        value_es_repository=value_es_repository,
                        column_qdrant_repository=column_qdrant_repository,
                        embedding_client=embedding_client)
