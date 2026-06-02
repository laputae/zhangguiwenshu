from typing import Annotated

from fastapi import Depends
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import meta_mysql_client_manager, dw_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager
from app.repositories.es.value_es_repository import ValueESRepository
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository
from app.services.query_service import QueryService


async def get_meta_session():
    async with meta_mysql_client_manager.session_factory() as session:
        yield session


async def get_dw_session():
    async with dw_mysql_client_manager.session_factory() as session:
        yield session


async def get_meta_mysql_repository(session: Annotated[AsyncSession, Depends(get_meta_session)]) -> MetaMySQLRepository:
    return MetaMySQLRepository(session)


async def get_dw_mysql_repository(session: Annotated[AsyncSession, Depends(get_dw_session)]) -> DWMySQLRepository:
    return DWMySQLRepository(session)


async def get_embedding_client() -> HuggingFaceEndpointEmbeddings:
    return embedding_client_manager.client


async def get_column_qdrant_repository() -> ColumnQdrantRepository:
    return ColumnQdrantRepository(qdrant_client_manager.client)


async def get_metric_qdrant_repository() -> MetricQdrantRepository:
    return MetricQdrantRepository(qdrant_client_manager.client)


async def get_value_es_repository() -> ValueESRepository:
    return ValueESRepository(es_client_manager.client)


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
