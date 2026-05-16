import uuid
from dataclasses import asdict
from pathlib import Path

from langchain_huggingface import HuggingFaceEndpointEmbeddings
from omegaconf import OmegaConf

from app.conf.meta_config import MetaConfig
from app.entities.column_info import ColumnInfo
from app.entities.table_info import TableInfo
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository


class MetaKnowledgeService:
    def __init__(self, meta_mysql_repository: MetaMySQLRepository,
                 dw_mysql_repository: DWMySQLRepository,
                 column_qdrant_repository: ColumnQdrantRepository,
                 embedding_client: HuggingFaceEndpointEmbeddings):
        self.meta_mysql_repository = meta_mysql_repository
        self.dw_mysql_repository = dw_mysql_repository
        self.column_qdrant_repository = column_qdrant_repository
        self.embedding_client: HuggingFaceEndpointEmbeddings = embedding_client

    async def build(self, config_path: Path):
        context = OmegaConf.load(config_path)
        schema = OmegaConf.structured(MetaConfig)
        meta_config: MetaConfig = OmegaConf.to_object(OmegaConf.merge(schema, context))
        if meta_config.tables:
            table_infos: list[TableInfo] = []
            column_infos: list[ColumnInfo] = []
            # 把配置文件的信息保存到meta数据库的column_info和table_info两个表中
            for table in meta_config.tables:
                table_info = TableInfo(id=table.name,
                                       name=table.name,
                                       role=table.role,
                                       description=table.description, )
                table_infos.append(table_info)
                column_types = await self.dw_mysql_repository.get_column_types(table.name)
                for column in table.columns:
                    column_values = await self.dw_mysql_repository.get_column_values(table.name, column.name)
                    column_info = ColumnInfo(id=f"{table.name}+{column.name}",
                                             name=column.name,
                                             type=column_types[column.name],
                                             role=column.role,
                                             examples=column_values,
                                             description=column.description,
                                             alias=column.alias,
                                             table_id=table.name)
                    column_infos.append(column_info)
            async with self.meta_mysql_repository.session.begin():
                await self.meta_mysql_repository.save_table_infos(table_infos)
                await self.meta_mysql_repository.save_column_infos(column_infos)
            # 对字段信息建立向量索引
            await self.column_qdrant_repository.ensure_collection()
            points: list[dict] = []
            for column_info in column_infos:
                points.append({
                    'id': uuid.uuid4(),
                    'embedding_text': column_info.name,
                    'payload': asdict(column_info)
                })
                points.append({
                    'id': uuid.uuid4(),
                    'embedding_text': column_info.description,
                    'payload': asdict(column_info)
                })
                for alia in column_info.alias:
                    points.append({
                        'id': uuid.uuid4(),
                        'embedding_text': alia,
                        'payload': asdict(column_info)
                    })
            embeddings: list[list[float]] = []
            embedding_texts = [point['embedding_text'] for point in points]
            embedding_batch_size = 20
            for i in range(0, len(embedding_texts), embedding_batch_size):
                batch_embedding_texts = embedding_texts[i:i + embedding_batch_size]
                batch_embeddings = await self.embedding_client.aembed_documents(batch_embedding_texts)
                embeddings.extend(batch_embeddings)

        if meta_config.metrics:
            pass
