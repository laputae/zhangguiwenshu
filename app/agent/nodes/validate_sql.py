from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository


async def validate_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    step = "验证SQL"
    writer({"type": "progress", "step": step, "status": "running"})
    try:
        sql = state["sql"]
        dw_mysql_repository: DWMySQLRepository = runtime.context["dw_mysql_repository"]
        try:
            await dw_mysql_repository.validate(sql)
            logger.info("SQL语法正确")
            writer({"type": "progress", "step": step, "status": "success"})
            return {"error": None}
        except Exception as e:
            logger.info(f"SQL语法错误: {str(e)}")
            writer({"type": "progress", "step": step, "statue": "success"})
            return {"error": str(e)}
    except Exception as e:
        logger.error(f"验证SQL失败: {str(e)}")
        writer({"type": "progress", "step": step, "status": "error"})
        raise
