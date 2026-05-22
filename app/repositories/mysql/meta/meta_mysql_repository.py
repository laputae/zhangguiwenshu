from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.column_info import ColumnInfo
from app.entities.column_metric import ColumnMetric
from app.entities.metric_info import MetricInfo
from app.entities.table_info import TableInfo
from app.repositories.mysql.meta.mappers.column_info_mapper import ColumnInfoMapper
from app.repositories.mysql.meta.mappers.column_metric_mapper import ColumnMetricMapper
from app.repositories.mysql.meta.mappers.metric_info_mapper import MetricInfoMapper
from app.repositories.mysql.meta.mappers.table_info_mapper import TableInfoMapper


class MetaMySQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_table_infos(self, table_infos: list[TableInfo]):
        self.session.add_all(TableInfoMapper.to_model(table_info) for table_info in table_infos)

    async def save_column_infos(self, column_infos: list[ColumnInfo]):
        self.session.add_all(ColumnInfoMapper.to_model(column_info) for column_info in column_infos)

    async def save_metric_infos(self, metric_infos:list[MetricInfo]):
        self.session.add_all(MetricInfoMapper.to_model(metric_info) for metric_info in metric_infos)

    async def save_column_metrics(self, column_metrics:list[ColumnMetric]):
        self.session.add_all(ColumnMetricMapper.to_model(column_metric) for column_metric in column_metrics)
