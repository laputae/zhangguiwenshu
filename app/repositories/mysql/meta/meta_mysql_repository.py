from sqlalchemy.ext.asyncio import AsyncSession


class MetaMySQLRepository:
    def __init__(self,session:AsyncSession):
        self.session=session

    async def save_table_infos(self, table_infos):
        self.session.add_all(table_infos)

    async def save_column_infos(self, column_infos):
        self.session.add_all(column_infos)
