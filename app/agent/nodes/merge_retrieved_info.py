import asyncio

from langgraph.runtime import Runtime
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.entities.column_info import ColumnInfo
from app.entities.metric_info import MetricInfo
from app.entities.value_info import ValueInfo


async def merge_retrieved_info(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("合并召回信息")

    retrieved_column_infos: list[ColumnInfo] = state["retrieved_column_infos"]
    retrieved_metric_infos: list[MetricInfo] = state["retrieved_metric_infos"]
    retrieved_value_infos: list[ValueInfo] = state["retrieved_value_infos"]
    # 将指标信息的相关字段信息添加到字段信息中
    retrieved_column_infos_map: dict[str, ColumnInfo] = {retrieved_column_info.id: retrieved_column_info for
                                                         retrieved_column_info in retrieved_column_infos}
    meta_mysql_repository = runtime.context["meta_mysql_repository"]
    for retrieved_metric_info in retrieved_metric_infos:
        for relevant_column in retrieved_metric_info.relevant_columns:
            if relevant_column not in retrieved_column_infos_map:
                column_info: ColumnInfo = await meta_mysql_repository.get_column_info_by_id(relevant_column)
                retrieved_column_infos_map[relevant_column] = column_info
    # 将字段取值加入到其所属字段的examples中
    for retrieved_value_info in retrieved_value_infos:
        value=retrieved_value_info.value
        column_id=retrieved_value_info.column_id
        if column_id not in retrieved_column_infos_map:
            column_info:ColumnInfo=await meta_mysql_repository.get_column_info_by_id(column_id)
            retrieved_column_infos_map[column_id] = column_info
        if value not in retrieved_column_infos_map[column_id].examples:
            retrieved_column_infos_map[column_id].examples.append(value)
    # 按照表对字段信息分组，整理成目标格式
