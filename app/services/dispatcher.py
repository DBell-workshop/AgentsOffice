"""调度员 Agent — 兼容层。

实际实现已拆分到 app.services.agents 包中。
此文件保留用于向后兼容现有 import 路径。
"""
from __future__ import annotations

# Re-export：保持所有现有 import 路径不变
from app.services.agents.definitions import BUILTIN_AGENTS  # noqa: F401
from app.services.agents.dispatcher import dispatch  # noqa: F401
from app.services.agents.registry import (  # noqa: F401
    build_dispatcher_prompt as _build_dispatcher_prompt,
    build_dispatcher_tools as _build_dispatcher_tools,
    load_agent_registry as _load_agent_registry,
)
from app.services.agents.runner import (  # noqa: F401
    record_cost as _record_cost,
    run_agent as _run_agent,
)
from app.services.agents.tools import (  # noqa: F401
    DATA_ANALYST_TOOLS,
    DATA_ENGINEER_TOOLS,
    DESIGNER_TOOLS,
    PRODUCT_TOOLS,
)
from app.services.agents.tool_executors import (  # noqa: F401
    execute_analyst_tool as _execute_analyst_tool,
    execute_data_tool as _execute_data_tool,
    execute_designer_tool as _execute_designer_tool,
    execute_product_tool as _execute_product_tool,
    generate_image as _generate_image,
)
