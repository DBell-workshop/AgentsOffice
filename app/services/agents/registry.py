"""Agent 注册表 — 从 DB 加载自定义配置，与内置默认合并。"""
from __future__ import annotations

import logging
from typing import Any, Dict, List

from app.services.agents.definitions import BUILTIN_AGENTS, DISPATCHER_DEFINITION

log = logging.getLogger(__name__)


def load_agent_registry() -> Dict[str, Dict[str, Any]]:
    """从 DB 加载活跃 Agent 定义，与内置默认合并。

    优先级：DB 自定义 > 内置默认。
    DB 中 active=True 的 agent 会覆盖内置默认。
    DB 中新增的 agent（不在内置列表中）也会被加入。
    """
    # 以内置默认为基础
    registry: Dict[str, Dict[str, Any]] = {}
    for slug, defn in BUILTIN_AGENTS.items():
        registry[slug] = {**defn, "slug": slug}

    # 从 DB 加载自定义配置
    try:
        from app.office.store import office_store
        if office_store is not None:
            db_agents = office_store.get_active_agent_definitions()
            for agent in db_agents:
                slug = agent["slug"]
                if slug == "dispatcher":
                    continue  # 调度员不作为可分配目标

                if slug in registry:
                    # DB 配置覆盖内置默认（仅覆盖非空字段）
                    if agent.get("system_prompt"):
                        registry[slug]["system_prompt"] = agent["system_prompt"]
                    if agent.get("display_name"):
                        registry[slug]["display_name"] = agent["display_name"]
                    if agent.get("role"):
                        registry[slug]["role"] = agent["role"]
                    if agent.get("color"):
                        registry[slug]["color"] = agent["color"]
                    if agent.get("room_id"):
                        registry[slug]["room_id"] = agent["room_id"]
                    if agent.get("phaser_agent_id"):
                        registry[slug]["phaser_agent_id"] = agent["phaser_agent_id"]
                    if agent.get("model_name"):
                        registry[slug]["model_name"] = agent["model_name"]
                else:
                    # 用户自定义的全新 Agent
                    if not agent.get("system_prompt"):
                        continue  # 没有提示词的 agent 无法工作
                    registry[slug] = {
                        "slug": slug,
                        "display_name": agent.get("display_name", slug),
                        "role": agent.get("role", ""),
                        "system_prompt": agent["system_prompt"],
                        "color": agent.get("color", "#cccccc"),
                        "room_id": agent.get("room_id", "workspace"),
                        "phaser_agent_id": agent.get("phaser_agent_id", ""),
                        "model_name": agent.get("model_name", ""),
                    }
    except Exception as e:
        log.warning("从 DB 加载 Agent 定义失败，使用内置默认: %s", e)

    return registry


def get_full_registry() -> Dict[str, Dict[str, Any]]:
    """返回完整注册表（含 dispatcher），供前端 API 使用。"""
    registry = load_agent_registry()
    # 加入调度员
    full = {"dispatcher": {**DISPATCHER_DEFINITION, "slug": "dispatcher"}}
    full.update(registry)
    return full


def build_dispatcher_prompt(registry: Dict[str, Dict[str, Any]]) -> str:
    """根据当前活跃 Agent 注册表动态构建调度员系统提示词。"""
    agent_descriptions = []
    for i, (slug, defn) in enumerate(registry.items(), 1):
        name = defn.get("display_name", slug)
        role = defn.get("role", "")
        agent_descriptions.append(
            f"{i}. **{name} ({slug})** — {role}"
        )

    agents_section = "\n".join(agent_descriptions)

    return f"""你是 AgentsOffice 的调度员（Dispatcher），负责理解用户需求并分配给合适的 Agent。

## 可用 Agent

{agents_section}

## 你的工作规则

- 分析用户的意图，决定交给谁处理
- 根据每个 Agent 的职责描述选择最合适的 Agent
- 如果需要多个 Agent 协作 → 说明协作方式
- 如果用户在闲聊/打招呼 → 你直接回复，不需要分配

## 输出格式

调用 assign_task 函数来分配任务。如果是闲聊，直接回复文字即可。"""


def build_dispatcher_tools(registry: Dict[str, Dict[str, Any]]) -> List[Dict]:
    """根据当前活跃 Agent 注册表动态构建调度员工具定义。"""
    agent_slugs = list(registry.keys())
    return [
        {
            "type": "function",
            "function": {
                "name": "assign_task",
                "description": "将用户任务分配给指定 Agent 执行",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_slug": {
                            "type": "string",
                            "enum": agent_slugs,
                            "description": "目标 Agent 标识",
                        },
                        "task_summary": {
                            "type": "string",
                            "description": "简要说明分配给 Agent 的任务内容",
                        },
                        "needs_collaboration": {
                            "type": "boolean",
                            "description": "是否需要多 Agent 协作",
                        },
                    },
                    "required": ["agent_slug", "task_summary"],
                },
            },
        }
    ]
