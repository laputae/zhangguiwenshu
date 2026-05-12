import asyncio

from requests import Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from app.conf.app_config import DBConfig, app_config


class MySQLClientManager:
    def __init__(self,config:DBConfig):
        self.engine:AsyncEngine|None=None
        self.config=config
        self.session_factory=None

    def _get_url(self):
        return f"mysql+asyncmy://{self.config.user}:{self.config.password}@{self.config.host}:{self.config.port}/{self.config.database}?charset=utf8mb4"
    def init(self):
        self.engine=create_async_engine(self._get_url(),pool_size=10,pool_pre_ping=True)
        self.session_factory=async_sessionmaker(self.engine,autoflush=True,expire_on_commit=False)
    async def close(self):
        await self.engine.dispose()

meta_mysql_client_manager=MySQLClientManager(app_config.db_meta)
dw_mysql_client_manager=MySQLClientManager(app_config.db_dw)

if __name__=="__main__":
    dw_mysql_client_manager.init()
    engine=dw_mysql_client_manager.engine
    async def test():
        async with dw_mysql_client_manager.session_factory() as session:
            sql="select * from fact_order"
            result=await session.execute(text(sql))
            rows=result.fetchall()
            print(type(rows))
            print(rows)
    asyncio.run(test())