"""调度员 — 理解用户意图，路由到合适的 Agent 执行。"""
from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, List, Optional

from app.services.llm_service import async_chat_completion
from app.services.agents.registry import (
    build_dispatcher_prompt,
    build_dispatcher_tools,
    load_agent_registry,
)
from app.services.agents.runner import record_cost, run_agent

log = logging.getLogger(__name__)


async def dispatch(
    user_message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    dispatcher_model: Optional[str] = None,
    agent_model: Optional[str] = None,
    agent_models: Optional[Dict[str, Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """执行完整的调度流程（异步）：用户消息 → 调度员路由 → Agent 执行。"""
    from app.models import make_id

    trace_id = make_id("trc")
    result_messages: List[Dict[str, Any]] = []

    # 动态加载 Agent 注册表
    registry = load_agent_registry()

    # 构建调度员消息（动态生成）
    dispatcher_prompt = build_dispatcher_prompt(registry)
    dispatcher_tools = build_dispatcher_tools(registry)

    messages = [{"role": "system", "content": dispatcher_prompt}]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    # 调度员自身的代理配置
    dispatcher_api_base = None
    dispatcher_api_key = None
    if agent_models and "dispatcher" in agent_models:
        dc = agent_models["dispatcher"]
        dispatcher_model = dispatcher_model or dc.get("model_name") or None
        dispatcher_api_base = dc.get("api_base") or None
        dispatcher_api_key = dc.get("api_key") or None

    # 调用调度员 LLM
    t0 = time.monotonic()
    dispatcher_result = await async_chat_completion(
        messages=messages,
        model=dispatcher_model,
        temperature=0.3,
        tools=dispatcher_tools,
        api_base=dispatcher_api_base,
        api_key=dispatcher_api_key,
    )
    dispatcher_ms = int((time.monotonic() - t0) * 1000)

    record_cost(
        agent_slug="dispatcher",
        trace_id=trace_id,
        model_name=dispatcher_result.get("model", dispatcher_model or "unknown"),
        usage=dispatcher_result["usage"],
        duration_ms=dispatcher_ms,
    )

    # 处理调度员响应
    tool_calls = dispatcher_result.get("tool_calls")

    if tool_calls:
        for tc in tool_calls:
            func = tc.get("function", {})
            func_name = func.get("name", "")

            if func_name == "assign_task":
                args = json.loads(func.get("arguments", "{}"))
                agent_slug = args.get("agent_slug", "shopping_guide")
                task_summary = args.get("task_summary", user_message)

                # 从注册表获取 Agent 信息
                agent_defn = registry.get(agent_slug, {})
                target_name = agent_defn.get("display_name", agent_slug)

                result_messages.append({
                    "role": "dispatcher",
                    "agent_slug": "dispatcher",
                    "agent_name": "调度员",
                    "content": f"收到，这个需求交给{target_name}处理。",
                    "usage": dispatcher_result["usage"],
                    "message_type": "routing",
                    "movement": {"agent_id": "agt_dispatcher", "room_id": "manager"},
                })

                # 确定目标模型和代理配置：per-agent 配置 > 全局 agent_model
                target_model = None
                target_api_base = None
                target_api_key = None
                if agent_models and agent_slug in agent_models:
                    ac = agent_models[agent_slug]
                    target_model = ac.get("model_name") or None
                    target_api_base = ac.get("api_base") or None
                    target_api_key = ac.get("api_key") or None
                target_model = target_model or agent_defn.get("model_name") or agent_model

                agent_response = await run_agent(
                    agent_slug=agent_slug,
                    agent_defn=agent_defn,
                    user_message=user_message,
                    task_summary=task_summary,
                    conversation_history=conversation_history,
                    model=target_model,
                    api_base=target_api_base,
                    api_key=target_api_key,
                )
                result_messages.extend(agent_response["messages"])
    else:
        result_messages.append({
            "role": "dispatcher",
            "agent_slug": "dispatcher",
            "agent_name": "调度员",
            "content": dispatcher_result["content"],
            "usage": dispatcher_result["usage"],
            "message_type": "response",
            "movement": None,
        })

    agent_movements = [
        msg["movement"] for msg in result_messages
        if msg.get("movement")
    ]

    return {
        "messages": result_messages,
        "agent_movements": agent_movements,
    }
