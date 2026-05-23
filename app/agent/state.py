from typing import TypedDict


class DataAgentState(TypedDict):
    # 校验SQL时出现的错误信息
    error: str
    
