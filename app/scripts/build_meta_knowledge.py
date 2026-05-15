import argparse
import asyncio
from pathlib import Path

from app.clients.mysql_client_manager import meta_mysql_client_manager, dw_mysql_client_manager
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta.meta_mysql_repository import MetaMySQLRepository
from app.services.meta_knowledge_service import MetaKnowledgeService


async def build(config_path: Path):
    meta_mysql_client_manager.init()
    dw_mysql_client_manager.init()
    async with (meta_mysql_client_manager.session_factory() as meta_session,
                dw_mysql_client_manager.session_factory() as dw_session):
        meta_mysql_repository = MetaMySQLRepository(meta_session)
        dw_mysql_repository = DWMySQLRepository(dw_session)
        meta_knowledge_service = MetaKnowledgeService(meta_mysql_repository,
                                                      dw_mysql_repository)
        await meta_knowledge_service.build(config_path)

    await meta_mysql_client_manager.close()
    await dw_mysql_client_manager.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf')
    args = parser.parse_args()
    config_path = args.conf

    asyncio.run(build(Path(config_path)))
