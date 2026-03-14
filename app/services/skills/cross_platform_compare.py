"""跨平台商品比价 Skill — Phase 1 Mock 实现。

状态机流程：
  INIT → on_start(query) → 搜索多平台 → yield 搜索结果 → AWAITING_USER
  AWAITING_USER → on_resume(selected_ids) → 执行比价分析 → yield 比价结论 → DONE
"""
from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from app.services.skills.base import BaseSkill, SkillState, SkillStepResult


# ============================================================
# Mock 多平台搜索数据（Phase 1）
# ============================================================

MOCK_SEARCH_RESULTS: Dict[str, List[Dict[str, Any]]] = {
    "京东": [
        {
            "product_id": "jd_10001",
            "name": "美的小厨宝 5L 速热即热式电热水器",
            "brand": "美的",
            "price": 399.0,
            "original_price": 499.0,
            "promotions": ["满300减50", "新用户券"],
            "rating": 4.8,
            "review_count": 12500,
            "platform": "京东",
            "url": "https://item.jd.com/mock_10001.html",
            "image_url": "",
        },
        {
            "product_id": "jd_10002",
            "name": "海尔小厨宝 6.6L 家用厨房电热水器",
            "brand": "海尔",
            "price": 459.0,
            "original_price": 599.0,
            "promotions": ["跨店满减"],
            "rating": 4.7,
            "review_count": 8900,
            "platform": "京东",
            "url": "https://item.jd.com/mock_10002.html",
            "image_url": "",
        },
        {
            "product_id": "jd_10003",
            "name": "史密斯小厨宝 5L 出水断电安全型",
            "brand": "A.O.Smith",
            "price": 699.0,
            "original_price": 799.0,
            "promotions": ["以旧换新补贴最高300"],
            "rating": 4.9,
            "review_count": 6700,
            "platform": "京东",
            "url": "https://item.jd.com/mock_10003.html",
            "image_url": "",
        },
    ],
    "淘宝": [
        {
            "product_id": "tb_20001",
            "name": "美的小厨宝 5升即热储水式厨房热水器",
            "brand": "美的",
            "price": 379.0,
            "original_price": 479.0,
            "promotions": ["淘金币抵扣", "店铺券满200减20"],
            "rating": 4.7,
            "review_count": 35000,
            "platform": "淘宝",
            "url": "https://item.taobao.com/mock_20001.html",
            "image_url": "",
        },
        {
            "product_id": "tb_20002",
            "name": "海尔6.6升小厨宝家用速热电热水器",
            "brand": "海尔",
            "price": 439.0,
            "original_price": 569.0,
            "promotions": ["88VIP 95折"],
            "rating": 4.6,
            "review_count": 21000,
            "platform": "淘宝",
            "url": "https://item.taobao.com/mock_20002.html",
            "image_url": "",
        },
    ],
    "拼多多": [
        {
            "product_id": "pdd_30001",
            "name": "美的5L小厨宝速热式厨房电热水器",
            "brand": "美的",
            "price": 349.0,
            "original_price": 399.0,
            "promotions": ["百亿补贴"],
            "rating": 4.5,
            "review_count": 50000,
            "platform": "拼多多",
            "url": "https://mobile.yangkeduo.com/mock_30001.html",
            "image_url": "",
        },
        {
            "product_id": "pdd_30002",
            "name": "海尔6.6L小厨宝即热式厨房电热水器",
            "brand": "海尔",
            "price": 419.0,
            "original_price": 529.0,
            "promotions": ["百亿补贴", "多人团再减10"],
            "rating": 4.5,
            "review_count": 28000,
            "platform": "拼多多",
            "url": "https://mobile.yangkeduo.com/mock_30002.html",
            "image_url": "",
        },
    ],
}


def _all_mock_products() -> List[Dict[str, Any]]:
    """展平所有平台的商品列表。"""
    products = []
    for platform_products in MOCK_SEARCH_RESULTS.values():
        products.extend(platform_products)
    return products


def _build_comparison(selected_ids: List[str]) -> Dict[str, Any]:
    """根据用户选择的商品构建比价结论。"""
    all_products = _all_mock_products()
    selected = [p for p in all_products if p["product_id"] in selected_ids]

    if not selected:
        return {"error": "未找到选择的商品"}

    selected.sort(key=lambda p: p["price"])
    cheapest = selected[0]
    most_expensive = selected[-1]
    savings = most_expensive["price"] - cheapest["price"]

    # 语义对齐（Phase 1 简化：同品牌 = 同款）
    brands = {p["brand"] for p in selected}
    if len(brands) == 1:
        comparison_type = "same_product"
        type_label = "同款商品跨平台比价"
    else:
        comparison_type = "similar_products"
        type_label = "同类商品横向对比"

    return {
        "comparison_type": comparison_type,
        "type_label": type_label,
        "products": selected,
        "cheapest": {
            "product_id": cheapest["product_id"],
            "name": cheapest["name"],
            "platform": cheapest["platform"],
            "price": cheapest["price"],
        },
        "price_range": {
            "min": cheapest["price"],
            "max": most_expensive["price"],
            "savings": savings,
        },
        "recommendation": (
            f"最低价在【{cheapest['platform']}】，"
            f"{cheapest['name']}，售价 ¥{cheapest['price']:.0f}"
            + (f"，比最高价便宜 ¥{savings:.0f}" if savings > 0 else "")
            + "。"
        ),
        "promotions_summary": {
            p["platform"]: p["promotions"] for p in selected
        },
    }


# ============================================================
# Skill 实现
# ============================================================

class CrossPlatformCompareSkill(BaseSkill):
    """跨平台商品比价 Skill。"""

    name = "cross_platform_compare"
    display_name = "跨平台比价"
    description = "在多个电商平台搜索同类商品，对比价格、促销和评价，给出购买建议"
    agent_slugs = ["shopping_guide"]

    async def on_start(self, params: Dict[str, Any]) -> SkillStepResult:
        """接收搜索关键词，返回多平台搜索结果。

        params: {"query": "小厨宝", "category": "热水器"}
        """
        query = params.get("query", "")

        # 模拟网络延迟
        await asyncio.sleep(0.3)

        # Phase 1: 返回全部 mock 数据
        search_results = dict(MOCK_SEARCH_RESULTS)
        total_count = sum(len(v) for v in search_results.values())

        events = [
            {
                "event": "skill_interact",
                "data": {
                    "interaction_type": "search_results",
                    "content": f"已在 {len(search_results)} 个平台找到 {total_count} 个相关商品",
                    "payload": {
                        "query": query,
                        "platforms": list(search_results.keys()),
                        "results": search_results,
                        "total_count": total_count,
                    },
                },
            },
        ]

        return SkillStepResult(
            next_state="awaiting_user",
            events=events,
            context_update={
                "query": query,
                "search_results": search_results,
            },
            user_prompt={
                "type": "select_products",
                "message": "请选择要对比的商品（2-4个）",
                "min_select": 2,
                "max_select": 4,
            },
        )

    async def on_resume(
        self,
        state: SkillState,
        context: Dict[str, Any],
        user_input: Any,
    ) -> SkillStepResult:
        """用户选择商品后执行比价分析。"""
        selected_ids = user_input.get("product_ids", [])

        # 模拟分析延迟
        await asyncio.sleep(0.5)

        comparison = _build_comparison(selected_ids)

        if "error" in comparison:
            return SkillStepResult(
                next_state="error",
                events=[
                    {
                        "event": "skill_error",
                        "data": {"error": comparison["error"]},
                    },
                ],
            )

        events = [
            {
                "event": "skill_interact",
                "data": {
                    "interaction_type": "comparison_result",
                    "content": comparison.get("recommendation", "比价分析完成"),
                    "payload": comparison,
                },
            },
        ]

        return SkillStepResult(
            next_state="done",
            events=events,
            context_update={
                "selected_ids": selected_ids,
                "comparison": comparison,
            },
        )

    def validate_user_input(
        self,
        state: SkillState,
        context: Dict[str, Any],
        user_input: Any,
    ) -> Optional[str]:
        if not isinstance(user_input, dict):
            return "输入格式错误，需要 {product_ids: [...]}"
        ids = user_input.get("product_ids")
        if not ids or not isinstance(ids, list):
            return "请选择至少2个商品进行对比"
        if len(ids) < 2:
            return "至少选择2个商品"
        if len(ids) > 4:
            return "最多选择4个商品"
        return None
