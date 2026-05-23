from langgraph.graph import StateGraph

from app.agent.context import DataAgentContext
from app.agent.nodes import extract_keywords, recall_metric, recall_value, filter_table, generate_sql, correct_sql, \
    validate_sql, run_sql
from app.agent.nodes.add_extra_context import add_extra_context
from app.agent.nodes.filter_metric import filter_metric
from app.agent.nodes.merge_retrieved_info import merge_retrieved_info
from app.agent.nodes.recall_column import recall_column
from app.agent.state import DataAgentState

graph_builder = StateGraph(state_schema=DataAgentState, context_schema=DataAgentContext)
graph_builder.add("extract_keywords", extract_keywords)
graph_builder.add("recall_column", recall_column)
graph_builder.add("recall_metric", recall_metric)
graph_builder.add("recall_value", recall_value)
graph_builder.add("merge_retrieved_info", merge_retrieved_info)
graph_builder.add("filter_metric", filter_metric)
graph_builder.add("filter_table", filter_table)
graph_builder.add("add_extra_context", add_extra_context)
graph_builder.add("generate_sql", generate_sql)
graph_builder.add("validate_sql", validate_sql)
graph_builder.add("correct_sql", correct_sql)
graph_builder.add("run_sql", run_sql)
