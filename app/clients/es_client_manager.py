import asyncio

from elasticsearch import AsyncElasticsearch

from app.conf.app_config import ESConfig, app_config


class ESClientManager:
    def __init__(self, config: ESConfig):
        self.client: AsyncElasticsearch | None = None
        self.config: ESConfig = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        self.client = AsyncElasticsearch(hosts=[self._get_url()])

    async def close(self):
        await self.client.close()
es_client_manager=ESClientManager(app_config.es)
if __name__ == "__main__":
    es_client_manager.init()
    client=es_client_manager.client
    async def test():
        await client.indices.create(
            index="test1",
        )
        await client.index(
            index="test1",
            document={
                "name": "test",
                "auther":"王八蛋",
                "release_date":"2000-01-01",
                "page_count":100,
            },
        )
        resp=await client.search(
            index="test1",
        )
        print(resp)
        await client.close()
    asyncio.run(test())
