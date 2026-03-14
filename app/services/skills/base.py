"""Skills 基础类 — 定义多步骤、有状态的 Agent 技能。

Skills 与 Tools 的区别：
- Tools：一次性 Function Calling，秒级完成，无状态
- Skills：多步骤状态机，支持用户交互暂停（awaiting_user），有会话上下文
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional


SkillState = Literal[
    "init",            # 初始化
    "running",         # 执行中
    "awaiting_user",   # 等待用户输入
    "done",            # 完成
    "error",           # 错误
]


@dataclass
class SkillStepResult:
    """单步执行结果。

    Skill 每一步返回此对象，由 SkillEngine 驱动状态转移。
    """

    next_state: SkillState
    events: List[Dict[str, Any]] = field(default_factory=list)
    context_update: Dict[str, Any] = field(default_factory=dict)
    user_prompt: Optional[Dict[str, Any]] = None

    @property
    def is_paused(self) -> bool:
        return self.next_state == "awaiting_user"

    @property
    def is_terminal(self) -> bool:
        return self.next_state in ("done", "error")


class BaseSkill(ABC):
    """所有 Skill 的抽象基类。

    子类需要实现 on_start / on_resume，并定义类属性 name / display_name / agent_slugs。
    """

    name: str = ""
    display_name: str = ""
    description: str = ""
    agent_slugs: List[str] = []

    @abstractmethod
    async def on_start(self, params: Dict[str, Any]) -> SkillStepResult:
        """Skill 启动时调用。

        Args:
            params: 触发参数，如 {"query": "小厨宝", "category": "热水器"}
        """
        ...

    @abstractmethod
    async def on_resume(
        self,
        state: SkillState,
        context: Dict[str, Any],
        user_input: Any,
    ) -> SkillStepResult:
        """用户响应后恢复执行。

        Args:
            state: 当前会话状态（通常是 "awaiting_user"）
            context: 会话上下文（之前步骤累积的数据）
            user_input: 用户提交的数据
        """
        ...

    def validate_user_input(
        self,
        state: SkillState,
        context: Dict[str, Any],
        user_input: Any,
    ) -> Optional[str]:
        """校验用户输入。返回 None 表示合法，返回字符串为错误信息。"""
        return None
