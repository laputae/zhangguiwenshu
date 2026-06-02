import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.api.schemas.query_schema import QuerySchema
from app.services.query_service import QueryService

query_router = APIRouter()


async def fake_streamer():
    for i in range(10):
        await asyncio.sleep(0.5)
        yield f"step:{i} "


async def get_query_service():
    return QueryService()


@query_router.post("/api/query")
async def query_handler(query: QuerySchema, query_service: Annotated[QueryService, Depends(get_query_service)]):
    return StreamingResponse(fake_streamer(), media_type="text/event-stream")
