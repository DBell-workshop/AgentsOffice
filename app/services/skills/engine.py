"""Skill 执行引擎 — 管理 SkillSession 生命周期。

Phase 1 使用内存存储会话状态，后续可迁移到数据库。
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Dict, List, Optional

from app.models import make_id, now_iso
from app.services.skills.base import SkillState
from app.services.skills.registry import get_skill

log = logging.getLogger(__name__)


@dataclass
class SkillSession:
    """一次 Skill 执行会话。"""

    session_id: str
    skill_name: str
    agent_slug: str
    state: SkillState = "init"
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = now_iso()
        if not self.updated_at:
            self.updated_at = now_iso()


# Phase 1: 内存存储
_sessions: Dict[str, SkillSession] = {}


class SkillEngine:
    """Skill 执行引擎，驱动 Skill 状态机并 yield SSE 事件。"""

    @staticmethod
    async def start_skill(
        skill_name: str,
        agent_slug: str,
        params: Dict[str, Any],
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """启动一个 Skill，yield SSE 事件流。"""
        skill = get_skill(skill_name)
        if skill is None:
            yield {
                "event": "skill_error",
                "data": {"error": f"未知 Skill: {skill_name}"},
            }
            return

        session_id = make_id("skl")
        session = SkillSession(
            session_id=session_id,
            skill_name=skill_name,
            agent_slug=agent_slug,
        )
        _sessions[session_id] = session

        yield {
            "event": "skill_start",
            "data": {
                "session_id": session_id,
                "skill_name": skill_name,
                "display_name": skill.display_name,
                "agent_slug": agent_slug,
            },
        }

        try:
            result = await skill.on_start(params)
        except Exception as e:
            log.error("Skill %s 启动失败: %s", skill_name, e)
            session.state = "error"
            session.context["error"] = str(e)
            session.updated_at = now_iso()
            yield {
                "event": "skill_error",
                "data": {"session_id": session_id, "error": str(e)},
            }
            return

        for evt in result.events:
            yield evt

        session.state = result.next_state
        session.context.update(result.context_update)
        session.updated_at = now_iso()

        if result.is_paused:
            yield {
                "event": "skill_interact",
                "data": {
                    "session_id": session_id,
                    "skill_name": skill_name,
                    "interaction_type": "awaiting_user",
                    "prompt": result.user_prompt or {},
                },
            }
        elif result.is_terminal:
            yield {
                "event": "skill_done",
                "data": {"session_id": session_id, "state": result.next_state},
            }

    @staticmethod
    async def respond_skill(
        session_id: str,
        user_input: Any,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """用户响应后恢复 Skill 执行。"""
        session = _sessions.get(session_id)
        if session is None:
            yield {
                "event": "skill_error",
                "data": {"error": f"会话不存在: {session_id}"},
            }
            return

        if session.state != "awaiting_user":
            yield {
                "event": "skill_error",
                "data": {
                    "session_id": session_id,
                    "error": f"会话状态非等待中: {session.state}",
                },
            }
            return

        skill = get_skill(session.skill_name)
        if skill is None:
            yield {
                "event": "skill_error",
                "data": {
                    "session_id": session_id,
                    "error": f"Skill 已失效: {session.skill_name}",
                },
            }
            return

        err = skill.validate_user_input(session.state, session.context, user_input)
        if err:
            yield {
                "event": "skill_error",
                "data": {"session_id": session_id, "error": err},
            }
            return

        try:
            result = await skill.on_resume(session.state, session.context, user_input)
        except Exception as e:
            log.error("Skill %s 恢复失败: %s", session.skill_name, e)
            session.state = "error"
            session.context["error"] = str(e)
            session.updated_at = now_iso()
            yield {
                "event": "skill_error",
                "data": {"session_id": session_id, "error": str(e)},
            }
            return

        for evt in result.events:
            yield evt

        session.state = result.next_state
        session.context.update(result.context_update)
        session.updated_at = now_iso()

        if result.is_paused:
            yield {
                "event": "skill_interact",
                "data": {
                    "session_id": session_id,
                    "skill_name": session.skill_name,
                    "interaction_type": "awaiting_user",
                    "prompt": result.user_prompt or {},
                },
            }
        elif result.is_terminal:
            yield {
                "event": "skill_done",
                "data": {"session_id": session_id, "state": result.next_state},
            }

    @staticmethod
    def get_session(session_id: str) -> Optional[SkillSession]:
        """获取会话信息。"""
        return _sessions.get(session_id)

    @staticmethod
    def list_active_sessions() -> List[Dict[str, Any]]:
        """列出所有活跃会话。"""
        return [
            {
                "session_id": s.session_id,
                "skill_name": s.skill_name,
                "agent_slug": s.agent_slug,
                "state": s.state,
                "created_at": s.created_at,
            }
            for s in _sessions.values()
            if s.state not in ("done", "error")
        ]
