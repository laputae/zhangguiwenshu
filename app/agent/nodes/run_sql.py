from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


async def run_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    step = "运行SQL"
    writer({"type": "progress", "step": step, "status": "running"})

    try:
        sql = state["sql"]
        dw_mysql_repository = runtime.context["dw_mysql_repository"]
        result = await dw_mysql_repository.run(sql)
        logger.info(f"SQL执行结果: {result}")
        writer({"type": "progress", "step": step, "status": "success"})
        return {"sql_result": result}
    except Exception as e:
        logger.error(f"运行SQL失败: {e}")
        writer({"type": "progress", "step": step, "status": "error"})
        raise
