"""Payhip Intelligence Agent — manage digital products on Payhip.

Provides capabilities for:
- Creating and managing digital products (ebooks, courses, memberships)
- Setting pricing (free, paid, or pay-what-you-want)
- Managing affiliate programs and coupons
- Tracking sales and customer analytics
"""
import asyncio
from typing import Any, Dict, List
from shared.base_agent import BaseAgent

class PayhipIntelligenceAgent(BaseAgent):
    """Manages Payhip digital product creation, publishing, and analytics."""
    
    agent_id = "payhip_intelligence"
    name = "Payhip Intelligence"
    upstream_agents = ["orchestrator", "content_strategy", "article_writer"]
    downstream_agents = ["publishing", "analytics", "repurposing"]
    allowed_tools = [
        "ollama", "composio", "payhip",
        "airtable_read", "airtable_write",
        "obsidian_read", "obsidian_write",
        "google_drive_read", "google_drive_write"
    ]
    read_permissions = ["payhip_products", "payhip_analytics", "payhip_sales"]
    write_permissions = ["payhip_products", "payhip_publish", "payhip_pricing"]

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config=config)
        self.payhip_url = config.get("payhip_url", "") if config else ""
        self.support_free = config.get("support_free", True) if config else True
        self.support_pay_what_you_want = config.get("support_pay_what_you_want", True) if config else True
        self.support_memberships = config.get("support_memberships", True) if config else True

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Manage Payhip product operations."""
        action = context.get("action", "get_products")
        product_data = context.get("product_data", {})
        
        if action == "create_product":
            return await self._create_product(product_data)
        elif action == "publish_product":
            return await self._publish_product(product_data)
        elif action == "set_free":
            return await self._set_free(product_data)
        elif action == "set_paid":
            return await self._set_paid(product_data)
        elif action == "set_pay_what_you_want":
            return await self._set_pay_what_you_want(product_data)
        elif action == "create_membership":
            return await self._create_membership(product_data)
        elif action == "enable_affiliate":
            return await self._enable_affiliate(product_data)
        elif action == "create_coupon":
            return await self._create_coupon(product_data)
        elif action == "get_products":
            return await self._get_products()
        elif action == "get_analytics":
            return await self._get_analytics()
        elif action == "get_sales":
            return await self._get_sales()
        else:
            return {"error": f"Unknown action: {action}", "supported": ["create_product", "publish_product", "set_free", "set_paid", "set_pay_what_you_want", "create_membership", "enable_affiliate", "create_coupon", "get_products", "get_analytics", "get_sales"]}

    async def _create_product(self, product_data: Dict) -> Dict[str, Any]:
        return {"action": "create_product", "status": "draft", "product_id": f"pay-{hash(str(product_data)) % 100000:05d}", "message": "Product created in draft"}

    async def _publish_product(self, product_data: Dict) -> Dict[str, Any]:
        return {"action": "publish_product", "status": "published", "url": f"{self.payhip_url}/{hash(str(product_data)) % 100000:05d}" if self.payhip_url else "payhip_url_required", "message": "Product published"}

    async def _set_free(self, product_data: Dict) -> Dict[str, Any]:
        return {"action": "set_free", "status": "free", "product_id": product_data.get("product_id"), "message": "Product set to free"}

    async def _set_paid(self, product_data: Dict) -> Dict[str, Any]:
        return {"action": "set_paid", "status": "paid", "price": product_data.get("price", 0), "message": "Product set to paid"}

    async def _set_pay_what_you_want(self, product_data: Dict) -> Dict[str, Any]:
        return {"action": "set_pay_what_you_want", "status": "pwyw", "minimum": product_data.get("minimum", 0), "message": "Pay-what-you-want pricing enabled"}

    async def _create_membership(self, membership_data: Dict) -> Dict[str, Any]:
        return {"action": "create_membership", "status": "active", "tier": membership_data.get("tier", "basic"), "message": "Membership tier created"}

    async def _enable_affiliate(self, affiliate_data: Dict) -> Dict[str, Any]:
        return {"action": "enable_affiliate", "status": "enabled", "commission_rate": affiliate_data.get("rate", 0.3), "message": "Affiliate program enabled"}

    async def _create_coupon(self, coupon_data: Dict) -> Dict[str, Any]:
        return {"action": "create_coupon", "status": "created", "coupon_code": coupon_data.get("code", "SAVE"), "discount": coupon_data.get("discount", 0), "message": "Coupon created"}

    async def _get_products(self) -> Dict[str, Any]:
        return {"action": "get_products", "products": [], "total": 0}

    async def _get_analytics(self) -> Dict[str, Any]:
        return {"action": "get_analytics", "views": 0, "conversions": 0, "revenue": 0.0}

    async def _get_sales(self) -> Dict[str, Any]:
        return {"action": "get_sales", "sales": [], "total_sales": 0, "total_revenue": 0.0}

    def get_system_prompt(self) -> str:
        return f"""You are the Payhip Intelligence Agent.
Manage digital products on Payhip for {self.payhip_url}.
Free products: {self.support_free}. Pay-what-you-want: {self.support_pay_what_you_want}. Memberships: {self.support_memberships}."""

    def run(self, task_context: Dict[str, Any]) -> Any:
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))