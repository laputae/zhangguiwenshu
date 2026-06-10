# 掌柜文书 (zhangguiwenshu)

基于 LLM 的自然语言数据查询系统。用户输入自然语言问题，系统自动理解语义、检索相关元数据、生成并执行 SQL，最终以 SSE 流式方式返回查询结果。

## 工作流

```
                             +-----------------+
                             | extract_keywords|  Jieba 分词抽取关键词
                             +-------+---------+
                                     |
              +----------------------+----------------------+
              |                      |                      |
              v                      v                      v
   +----------+------+   +----------+------+   +----------+------+
   |  recall_column  |   |  recall_metric  |   |  recall_value   |
   |  Qdrant 向量召回 |   |  Qdrant 向量召回 |   |  ES 全文检索     |
   +----------+------+   +----------+------+   +----------+------+
              |                      |                      |
              +----------------------+----------------------+
                                     |
                          +----------v---------+
                          | merge_retrieved_info|
                          +----------+---------+
                                     |
                   +-----------------+------------------+
                   |                                    |
          +--------v--------+              +------------v--------+
          |   filter_table   |              |   filter_metric    |
          |   LLM 过滤表信息  |              |   LLM 过滤指标信息   |
          +--------+--------+              +----------+---------+
                   |                                    |
                   +-----------------+------------------+
                                     |
                          +----------v---------+
                          | add_extra_context  |  附加日期/DB信息
                          +----------+---------+
                                     |
                          +----------v---------+
                          |   generate_sql    |  LLM 生成 SQL
                          +----------+---------+
                                     |
                          +----------v---------+
                          |   validate_sql    |  EXPLAIN 校验
                          +----------+---------+
                             |           |
                        error=N     error=有
                             |           |
                             v           v
                   +---------+--+   +----+--------+
                   |   run_sql   |   | correct_sql |  LLM 纠错
                   +---------+--+   +----+--------+
                             |           |
                             v           v
                            END <--------+
```

## 项目架构

```
main.py                         # FastAPI 应用入口
├── app/
│   ├── api/                    # HTTP API 层
│   │   ├── routers/            # 路由（POST /api/query）
│   │   ├── schemas/            # 请求模型
│   │   ├── dependencies.py     # 依赖注入（资源装配）
│   │   └── lifespan.py         # 应用生命周期（启动初始化/关闭释放）
│   ├── agent/                  # LangGraph 智能体
│   │   ├── graph.py            # 工作流编排（DAG + 条件分支）
│   │   ├── state.py            # Agent 状态定义（TypedDict）
│   │   ├── context.py          # Agent 上下文（运行时资源注入）
│   │   ├── llm.py              # LLM 初始化（DeepSeek via LangChain）
│   │   └── nodes/              # 12 个工作流节点
│   ├── services/               # 业务服务
│   │   ├── query_service.py    # 查询服务（编排 Agent 执行）
│   │   └── meta_knowledge_service.py  # 元知识构建（向量化+索引）
│   ├── repositories/           # 数据访问层（读写分离）
│   │   ├── mysql/meta/         # 元数据库 CRUD
│   │   ├── mysql/dw/           # 数据仓库（查询+校验）
│   │   ├── qdrant/             # 向量检索
│   │   └── es/                 # 全文检索
│   ├── clients/                # 连接管理器（MySQL/Qdrant/ES/Embedding）
│   ├── models/                 # SQLAlchemy ORM 模型
│   ├── entities/               # 领域实体（dataclass）
│   ├── conf/                   # 配置数据类（OmegaConf + dataclass）
│   ├── core/                   # 日志（Loguru + request_id 注入）
│   ├── prompt/                 # Prompt 模板加载器
│   └── scripts/                # CLI 脚本
├── conf/                       # YAML 配置文件
│   ├── app_config.yaml         # 基础设施连接配置
│   └── meta_config.yaml        # 数据表/字段/指标元数据定义
└── prompts/                    # Prompt 模板文件
```

## 技术栈

| 分类 | 技术 | 用途 |
|------|------|------|
| Web 框架 | FastAPI | HTTP 服务 + SSE 流式响应 |
| AI 编排 | LangGraph | 多节点 Agent 工作流 |
| LLM | DeepSeek API (via LangChain) | SQL 生成/纠错/过滤 |
| 向量数据库 | Qdrant | 字段/指标语义检索 |
| 全文检索 | Elasticsearch | 维度字段取值检索 |
| 分词 | Jieba | 查询关键词抽取 |
| 嵌入模型 | BAAI/bge-large-zh-v1.5 | 中文文本向量化（HuggingFace Endpoint） |
| 关系数据库 | MySQL + SQLAlchemy + asyncmy | 元数据存储 + 数据仓库查询 |
| 配置管理 | OmegaConf | YAML → dataclass 映射 |
| 日志 | Loguru | 结构化日志 + request_id 追踪 |
| 包管理 | uv | 依赖管理与环境同步 |

## 快速开始

### 环境要求

| 组件 | 说明 |
|------|------|
| Python >= 3.12 | 运行时 |
| [uv](https://docs.astral.sh/uv/) | 包管理器 |
| MySQL | 需要 `meta` 和 `dw` 两个数据库 |
| Qdrant | 向量数据库 |
| Elasticsearch | 全文检索引擎 |
| HuggingFace Embedding Service | 文本向量化服务 |
| DeepSeek API Key | LLM 调用 |

### 安装

```bash
# 克隆项目
git clone <repo-url> && cd zhangguiwenshu

# 安装依赖
uv sync

# 设置环境变量
export DEEPSEEK_API_KEY=your_api_key
```

### 配置基础设施

编辑 `conf/app_config.yaml`，配置各服务连接信息：

```yaml
db_meta:        # 元数据库（存储表/字段/指标元数据），需预先创建空库
db_dw:          # 数据仓库（存放实际的业务数据表）
qdrant:         # 向量数据库
embedding:      # HuggingFace Embedding 服务的地址和模型
es:             # Elasticsearch
llm:            # LLM 配置（默认 DeepSeek，也可换成 OpenAI 兼容接口）
```

### 创建 meta 数据库表

项目使用 SQLAlchemy ORM，需要先在 meta 库中创建以下表。在 Python 中执行：

```python
from app.clients.mysql_client_manager import meta_mysql_client_manager
from app.models.base import Base

meta_mysql_client_manager.init()
async with meta_mysql_client_manager.engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
await meta_mysql_client_manager.close()
```

meta 库将生成 4 张表：`table_info`、`column_info`、`metric_info`、`column_metric`。

### 定义元数据

编辑 `conf/meta_config.yaml`，定义你的数据表结构和指标：

```yaml
tables:
  - name: dim_region          # 表名（必须与 dw 库中的实际表名一致）
    role: dim                  # dim=维度表 / fact=事实表
    description: 地区维度表     # 表用途描述（用于 LLM 上下文）
    columns:
      - name: region_id
        role: primary_key      # primary_key / foreign_key / dimension / measure
        description: 地区唯一标识
        alias: [地区ID, 区域ID]  # 字段别名（提升搜索召回率）
        sync: false             # 是否将该字段的取值同步到 ES 做全文检索

      - name: region_name
        role: dimension
        description: 大区名称，如华东、华南
        alias: [地区, 区域, 大区]
        sync: true              # 维度字段建议开启同步

metrics:
  - name: GMV
    description: 所有订单的成交金额总和
    alias: [成交总额, 订单总额]
    relevant_columns:            # 该指标涉及的事实表字段（格式：表名.字段名）
      - fact_order.order_amount
```

**字段说明：**

- `tables[].role`: `dim`（维度表）或 `fact`（事实表）
- `columns[].role`: `primary_key` / `foreign_key` / `dimension`（维度字段）/ `measure`（度量字段）
- `columns[].sync`: `true` 表示从 dw 库拉取该字段的去重取值并索引到 ES，通常维度字段开启
- `metrics[].relevant_columns`: 关联的事实表度量字段，LLM 生成 SQL 时的关键参考

### 构建元知识库

```bash
python -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
```

该脚本完成：
1. 读取 dw 库获取实际字段类型和取值
2. 将表/字段/指标元数据写入 meta 库
3. 为字段和指标生成向量（via Embedding Service）并写入 Qdrant
4. 将 `sync: true` 的字段取值同步到 Elasticsearch

### 启动服务

```bash
uv run main.py
# 或
fastapi dev main.py
```

### API 调用

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "统计华北地区的销售总额"}'
```

接口返回 SSE（Server-Sent Events）流，响应格式如下：

```
data: {"type":"progress","step":"抽取关键词","status":"running"}
data: {"type":"progress","step":"抽取关键词","status":"success"}
data: {"type":"progress","step":"召回字段","status":"running"}
data: {"type":"progress","step":"召回字段","status":"success"}
data: {"type":"progress","step":"召回取值","status":"running"}
data: {"type":"progress","step":"召回取值","status":"success"}
data: {"type":"progress","step":"召回指标","status":"running"}
data: {"type":"progress","step":"召回指标","status":"success"}
data: {"type":"progress","step":"合并检索信息","status":"running"}
data: {"type":"progress","step":"合并检索信息","status":"success"}
data: {"type":"progress","step":"过滤表","status":"running"}
data: {"type":"progress","step":"过滤表","status":"success"}
data: {"type":"progress","step":"过滤指标","status":"running"}
data: {"type":"progress","step":"过滤指标","status":"success"}
data: {"type":"progress","step":"生成SQL","status":"running"}
data: {"type":"progress","step":"生成SQL","status":"success"}
data: {"type":"progress","step":"验证SQL","status":"running"}
data: {"type":"progress","step":"验证SQL","status":"success"}
data: {"type":"progress","step":"运行SQL","status":"running"}
data: {"type":"progress","step":"运行SQL","status":"success"}
data: {"type":"result","data":[{"region_name":"华北","total_amount":1234567.89}]}
```

- `type: "progress"` — 流程进度通知，`status` 取值 `running` / `success` / `error`
- `type: "result"` — SQL 执行结果，`data` 为查询返回的行列表
- `type: "error"` — 错误信息

## 常见问题

**Q: Embedding 服务如何启动？**

使用 HuggingFace TEI (Text Embeddings Inference) 部署：

```bash
docker run -p 8081:80 -e MODEL_ID=BAAI/bge-large-zh-v1.5 \
  ghcr.io/huggingface/text-embeddings-inference:latest
```

**Q: 可以更换其他 LLM 吗？**

可以。修改 `conf/app_config.yaml` 中的 `llm` 配置段。项目使用 `langchain.chat_models.init_chat_model` 初始化，支持 OpenAI 兼容接口。

**Q: SQL 校验是怎么实现的？**

使用 MySQL 的 `EXPLAIN` 语句对生成的 SQL 做语法校验。如果 SQL 语法有误，会自动进入 `correct_sql` 节点由 LLM 修复后重新校验。
