"""Agent 工具定义 — 各类 Agent 可用的 Function Calling 工具 Schema。"""
from __future__ import annotations

from typing import Any, Dict, List


# ============================================================
# 数据工程师专属工具
# ============================================================
DATA_ENGINEER_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "analyze_uploaded_file",
            "description": "分析已上传的文件（CSV/Excel），返回列名、数据类型、预览数据。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文件路径（从 list_uploaded_files 获取）",
                    },
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_table_from_file",
            "description": "根据已上传的文件自动创建数据库表并导入全部数据。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文件路径",
                    },
                    "table_name": {
                        "type": "string",
                        "description": "自定义表名（可选）",
                    },
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_sql",
            "description": "执行 SQL 语句。支持 SELECT、CREATE TABLE、ALTER TABLE 等操作。",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "要执行的 SQL 语句",
                    },
                },
                "required": ["sql"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_user_tables",
            "description": "列出用户创建的所有数据表",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_data",
            "description": "查询用户表中的数据，支持 WHERE 条件筛选",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "表名",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回行数上限，默认 50",
                    },
                    "where": {
                        "type": "string",
                        "description": "WHERE 条件（如 price > 100）",
                    },
                },
                "required": ["table_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_uploaded_files",
            "description": "列出所有已上传的文件",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "clean_data",
            "description": "按规则清洗数据文件。支持：填充空值、删除空值行、去重、列重命名、值统一。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "要清洗的文件路径",
                    },
                    "rules": {
                        "type": "object",
                        "description": "清洗规则",
                    },
                },
                "required": ["file_path", "rules"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "test_db_connection",
            "description": "测试外部数据库连接。",
            "parameters": {
                "type": "object",
                "properties": {
                    "db_type": {
                        "type": "string",
                        "enum": ["postgresql", "mysql", "sqlite"],
                        "description": "数据库类型",
                    },
                    "host": {"type": "string", "description": "主机地址"},
                    "port": {"type": "integer", "description": "端口号"},
                    "database": {"type": "string", "description": "数据库名称"},
                    "username": {"type": "string", "description": "用户名"},
                    "password": {"type": "string", "description": "密码"},
                },
                "required": ["db_type", "host", "port", "database", "username", "password"],
            },
        },
    },
]


# ============================================================
# 数据分析师专属工具
# ============================================================
DATA_ANALYST_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "query_office_costs",
            "description": "查询 AgentsOffice 的 LLM 调用成本数据",
            "parameters": {
                "type": "object",
                "properties": {
                    "view": {
                        "type": "string",
                        "enum": ["by_agent", "by_model", "summary"],
                        "description": "查看维度",
                    },
                    "start": {"type": "string", "description": "起始时间（ISO格式）"},
                    "end": {"type": "string", "description": "结束时间（ISO格式）"},
                },
                "required": ["view"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_agent_stats",
            "description": "查询各 Agent 的工作状态统计",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_sql",
            "description": "执行自定义 SQL 查询进行深度数据分析",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {"type": "string", "description": "要执行的 SQL 语句"},
                },
                "required": ["sql"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_user_tables",
            "description": "列出所有可查询的用户数据表",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_data",
            "description": "查询用户表中的数据，支持 WHERE 条件",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名"},
                    "limit": {"type": "integer", "description": "返回行数上限"},
                    "where": {"type": "string", "description": "WHERE 条件"},
                },
                "required": ["table_name"],
            },
        },
    },
]


def get_tools_by_key(tools_key: str) -> List[Dict[str, Any]]:
    """根据 tools_key 字符串返回对应的工具列表。"""
    _TOOLS_MAP = {
        "DATA_ENGINEER_TOOLS": DATA_ENGINEER_TOOLS,
        "DATA_ANALYST_TOOLS": DATA_ANALYST_TOOLS,
    }
    return _TOOLS_MAP.get(tools_key, [])
