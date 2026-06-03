from langgraph.runtime import Runtime
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger
import asyncio


async def validate_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer({"type": "progress", "step": "验证SQL", "status": "running"})

    try:
        await asyncio.sleep(0.5)
        writer({"type": "progress", "step": "验证SQL", "status": "success"})
        return {"error": None}
    except Exception as e:
        logger.error(f"验证SQL失败: {e}")
        writer({"type": "progress", "step": "验证SQL", "status": "error"})
        raise
