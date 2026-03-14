"""LLM 统一调用层 — 基于 LiteLLM 支持多家模型。"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple

import litellm

from app.config import settings

# LiteLLM 全局配置
litellm.drop_params = True  # 自动忽略模型不支持的参数

# DashScope (阿里云百炼) OpenAI 兼容端点
_DASHSCOPE_API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"


def _ensure_api_keys():
    """将 settings 中的 API Key 注入环境变量（LiteLLM 从环境变量读取）。"""
    if settings.gemini_api_key:
        os.environ.setdefault("GEMINI_API_KEY", settings.gemini_api_key)
    if settings.anthropic_api_key:
        os.environ.setdefault("ANTHROPIC_API_KEY", settings.anthropic_api_key)
    if settings.openai_api_key:
        os.environ.setdefault("OPENAI_API_KEY", settings.openai_api_key)
    if settings.deepseek_api_key:
        os.environ.setdefault("DEEPSEEK_API_KEY", settings.deepseek_api_key)


_ensure_api_keys()


def _resolve_model(
    model: str,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Tuple[str, Optional[str], Optional[str]]:
    """自动识别模型所属平台，注入对应的 api_base 和 api_key。

    当调用方已显式传入 api_base/api_key 时，不做覆盖。
    目前支持自动识别：
      - Qwen 系列 → 阿里云百炼 DashScope
    """
    if api_base or api_key:
        return model, api_base, api_key

    # Qwen 模型 → DashScope
    model_lower = model.lower()
    if ("qwen" in model_lower) and settings.dashscope_api_key:
        # 确保模型名有 openai/ 前缀（LiteLLM 的 OpenAI 兼容模式）
        clean_name = model.split("/", 1)[-1] if "/" in model else model
        return f"openai/{clean_name}", _DASHSCOPE_API_BASE, settings.dashscope_api_key

    return model, api_base, api_key


def chat_completion(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    tools: Optional[List[Dict[str, Any]]] = None,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """同步调用 LLM，返回标准化结果。

    Args:
        messages: OpenAI 格式消息列表 [{"role": "system", "content": "..."}]
        model: 模型标识，如 "gemini/gemini-2.0-flash"、"qwen-plus"
        temperature: 生成温度
        max_tokens: 最大输出 token
        tools: Function Calling 工具定义（可选）
        api_base: 自定义代理地址（如 one-api/new-api 等），可选
        api_key: 自定义 API Key（配合 api_base 使用），可选

    Returns:
        {
            "content": "模型回复文本",
            "tool_calls": [...] 或 None,
            "model": "实际使用的模型",
            "usage": {"input_tokens": N, "output_tokens": N, "total_tokens": N}
        }
    """
    model = model or settings.default_llm_model
    model, api_base, api_key = _resolve_model(model, api_base, api_key)

    kwargs: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if tools:
        kwargs["tools"] = tools
    if api_base:
        kwargs["api_base"] = api_base
    if api_key:
        kwargs["api_key"] = api_key

    response = litellm.completion(**kwargs)
    return _parse_response(response, model)


async def async_chat_completion(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    tools: Optional[List[Dict[str, Any]]] = None,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """异步调用 LLM，返回标准化结果。参数与 chat_completion 相同。"""
    model = model or settings.default_llm_model
    model, api_base, api_key = _resolve_model(model, api_base, api_key)

    kwargs: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if tools:
        kwargs["tools"] = tools
    if api_base:
        kwargs["api_base"] = api_base
    if api_key:
        kwargs["api_key"] = api_key

    response = await litellm.acompletion(**kwargs)
    return _parse_response(response, model)


def _parse_response(response: Any, model: str) -> Dict[str, Any]:
    """将 LiteLLM 响应解析为标准化 dict。"""
    choice = response.choices[0]
    usage = response.usage

    return {
        "content": choice.message.content or "",
        "tool_calls": (
            [tc.model_dump() for tc in choice.message.tool_calls]
            if choice.message.tool_calls
            else None
        ),
        "model": response.model or model,
        "usage": {
            "input_tokens": usage.prompt_tokens if usage else 0,
            "output_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
        },
    }
