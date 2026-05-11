import asyncio
from typing import Optional
from langchain_openai import OpenAIEmbeddings

from app.conf.app_config import EmbeddingConfig, app_config


class EmbeddingClientManager:
    def __init__(self, config: EmbeddingConfig):
        self.client: Optional[OpenAIEmbeddings] = None
        self.config = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}/v1"

    def init(self):
        self.client = OpenAIEmbeddings(
            model="text-embedding-v1",  # 这里填入你本地模型实际的名字，或者随便填一个字符串
            openai_api_base=self._get_url(),
            openai_api_key="sk-no-key-needed",  # 本地服务通常不需要 key，但该字段必填
            check_embedding_ctx_length=False  # 建议关闭，防止本地接口不支持长度检查而报错
        )


embedding_client_manager = EmbeddingClientManager(app_config.embedding)


if __name__ == "__main__":
    embedding_client_manager.init()
    client = embedding_client_manager.client
    async def test():
        text = "逸一时误一世"
        query_result =await client.aembed_query(text)
        print(query_result)

    asyncio.run(test())
