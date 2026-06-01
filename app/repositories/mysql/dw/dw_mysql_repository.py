from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


class DWMySQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_column_types(self, table_name) -> dict[str, str]:
        sql = f"show columns from {table_name}"
        result = await self.session.execute(text(sql))
        result_dict = result.mappings().fetchall()
        return {row['Field']: row['Type'] for row in result_dict}

    async def get_column_values(self, table_name, column_name, limit=10):
        sql = f"select distinct {column_name} from {table_name} limit {limit}"
        result = await self.session.execute(text(sql))
        return [r[0] for r in result.fetchall()]

    async def get_db_info(self):
        sql = "select version()"
        result = await self.session.execute(text(sql))
        version = result.scalar()
        dialect = self.session.bind.dialect.name
        return {"dialect": dialect, "version": version}
