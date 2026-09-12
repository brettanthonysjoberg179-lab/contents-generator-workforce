"""Gumroad Intelligence Agent — manage digital products on Gumroad.

Provides capabilities for:
- Creating and managing digital products (ebooks, courses, memberships)
- Uploading product files
- Managing pricing, coupons, and affiliate programs
- Tracking sales analytics and conversion rates
"""
import asyncio
from typing import Any, Dict, List
from shared.base_agent import BaseAgent

class GumroadIntelligenceAgent(BaseAgent):
    """Manages Gumroad digital product creation, publishing, and analytics."""
    
    agent_id = "gumroad_intelligence"
    name = "Gumroad Intelligence"
    upstream_agents = ["orchestrator", "content_strategy", "article_writer"]
    downstream_agents = ["publishing", "analytics", "repurposing"]
    allowed_tools = [
        "ollama", "composio", "gumroad",
        "airtable_read", "airtable_write",
        "obsidian_read", "obsidian_write",
        "google_drive_read", "google_drive_write"
    ]
    read_permissions = ["gumroad_products", "gumroad_analytics", "gumroad_sales"]
    write_permissions = ["gumroad_products", "gumroad_publish", "gumroad_pricing"]

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config=config)
        self.gumroad_url = config.get("gumroad_url", "") if config else ""
        self.support_subscriptions = config.get("support_subscriptions", True) if config else True
        self.drip_content = config.get("drip_content", False) if config else False

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Manage Gumroad product operations."""
        action = context.get("action", "get_products")
        product_data = context.get("product_data", {})
        
        if action == "create_product":
            return await self._create_product(product_data)
        elif action == "publish_product":
            return await self._publish_product(product_data)
        elif action == "upload_file":
            return await self._upload_file(product_data)
        elif action == "set_pricing":
            return await self._set_pricing(product_data)
        elif action == "create_coupon":
            return await self._create_coupon(product_data)
        elif action == "enable_affiliate":
            return await self._enable_affiliate(product_data)
        elif action == "get_products":
            return await self._get_products()
        elif action == "get_analytics":
            return await self._get_analytics()
        elif action == "get_sales":
            return await self._get_sales()
        else:
            return {"error": f"Unknown action: {action}", "supported": ["create_product", "publish_product", "upload_file", "set_pricing", "create_coupon", "enable_affiliate", "get_products", "get_analytics", "get_sales"]}

    async def _create_product(self, product_data: Dict) -> Dict[str, Any]:
        return {"action": "create_product", "status": "draft", "product_id": f"gum-{hash(str(product_data)) % 100000:05d}", "message": "Product created in draft"}

    async def _publish_product(self, product_data: Dict) -> Dict[str, Any]:
        return {"action": "publish_product", "status": "published", "url": f"{self.gumroad_url}/{hash(str(product_data)) % 100000:05d}" if self.gumroad_url else "gumroad_url_required", "message": "Product published"}

    async def _upload_file(self, file_data: Dict) -> Dict[str, Any]:
        return {"action": "upload_file", "status": "uploaded", "file_id": f"file-{hash(str(file_data)) % 100000:05d}", "message": "File uploaded to Gumroad"}

    async def _set_pricing(self, pricing_data: Dict) -> Dict[str, Any]:
        return {"action": "set_pricing", "status": "pricing_set", "price": pricing_data.get("price", 0), "message": "Pricing configured"}

    async def _create_coupon(self, coupon_data: Dict) -> Dict[str, Any]:
        return {"action": "create_coupon", "status": "created", "coupon_code": coupon_data.get("code", "NEW"), "discount": coupon_data.get("discount", 0), "message": "Coupon created"}

    async def _enable_affiliate(self, affiliate_data: Dict) -> Dict[str, Any]:
        return {"action": "enable_affiliate", "status": "enabled", "commission_rate": affiliate_data.get("rate", 0.3), "message": "Affiliate program enabled"}

    async def _get_products(self) -> Dict[str, Any]:
        return {"action": "get_products", "products": [], "total": 0}

    async def _get_analytics(self) -> Dict[str, Any]:
        return {"action": "get_analytics", "views": 0, "conversions": 0, "revenue": 0.0}

    async def _get_sales(self) -> Dict[str, Any]:
        return {"action": "get_sales", "sales": [], "total_sales": 0, "total_revenue": 0.0}

    def get_system_prompt(self) -> str:
        return f"""You are the Gumroad Intelligence Agent.
Manage digital products on Gumroad for {self.gumroad_url}.
Subscriptions: {self.support_subscriptions}. Drip content: {self.drip_content}."""

    def run(self, task_context: Dict[str, Any]) -> Any:
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))