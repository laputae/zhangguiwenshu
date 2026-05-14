import asyncio
from pathlib import Path
from app.conf.meta_config import MetaConfig

from omegaconf import OmegaConf


class MetaKnowledgeService:
    def __init__(self):
        pass

    async def build(self, config_path: Path):
        context = OmegaConf.load(config_path)
        schema = OmegaConf.structured(MetaConfig)
        meta_config: MetaConfig = OmegaConf.to_object(OmegaConf.merge(schema, context))
        print(meta_config.metrics)
        if meta_config.tables:
            # 把配置文件的信息保存到meta数据库的column_info和table_info两个表中
            
            pass
        if meta_config.metrics:
            pass
