from langgraph.runtime import Runtime
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
import asyncio


async def validate_sql(state:DataAgentState,runtime:Runtime[DataAgentContext]):
    writer=runtime.stream_writer
    writer("验证SQL")
    await asyncio.sleep(0.5)
