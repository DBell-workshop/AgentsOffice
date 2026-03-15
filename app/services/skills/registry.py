"""Skill 注册表 — 全局 Skill 实例管理。

通用版不预装任何 Skill。用户可通过继承 BaseSkill 自定义技能并注册。
"""
from __future__ import annotations

from typing import Dict, List, Optional

from app.services.skills.base import BaseSkill

_SKILL_REGISTRY: Dict[str, BaseSkill] = {}
_initialized = False


def register_skill(skill: BaseSkill) -> None:
    """注册一个 Skill 实例到全局注册表。"""
    _SKILL_REGISTRY[skill.name] = skill


def get_skill(name: str) -> Optional[BaseSkill]:
    """按名称查找 Skill。"""
    _ensure_initialized()
    return _SKILL_REGISTRY.get(name)


def list_skills() -> List[Dict[str, str]]:
    """返回所有已注册 Skill 的摘要信息。"""
    _ensure_initialized()
    return [
        {
            "name": s.name,
            "display_name": s.display_name,
            "description": s.description,
            "agent_slugs": s.agent_slugs,
        }
        for s in _SKILL_REGISTRY.values()
    ]


def get_skills_for_agent(agent_slug: str) -> List[BaseSkill]:
    """返回某个 Agent 可用的所有 Skill。"""
    _ensure_initialized()
    return [
        s for s in _SKILL_REGISTRY.values()
        if agent_slug in s.agent_slugs
    ]


def _ensure_initialized() -> None:
    """延迟注册内置 Skill。通用版无预装 Skill。"""
    global _initialized
    if _initialized:
        return
    _initialized = True
    # 用户自定义 Skill 可在此处注册，例如:
    # from my_skills.example import ExampleSkill
    # register_skill(ExampleSkill())
