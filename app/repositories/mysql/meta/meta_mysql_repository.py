from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.column_info import ColumnInfo
from app.entities.table_info import TableInfo


class MetaMySQLRepository:
    def __init__(self,session:AsyncSession):
        self.session=session

    async def save_table_infos(self, table_infos:list[TableInfo]):
        self.session.add_all(table_infos)

    async def save_column_infos(self, column_infos:list[ColumnInfo]):
        self.session.add_all(column_infos)
