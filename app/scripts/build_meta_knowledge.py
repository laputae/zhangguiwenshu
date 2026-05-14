import argparse
import asyncio
from pathlib import Path

from app.services.meta_knowledge_service import MetaKnowledgeService


async def build(config_path: Path):
    meta_knowledge_service=MetaKnowledgeService()
    await meta_knowledge_service.build(config_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf')
    args = parser.parse_args()
    config_path = args.conf

    asyncio.run(build(Path(config_path)))
