from shared.base_agent import BaseAgent
from shared.database_manager import DatabaseManager
from typing import Any, Dict

class ProductsPackagerAgent(BaseAgent):
    """
    Specialized agent for bundling digital products and managing metadata.
    """
    def __init__(self, db: DatabaseManager):
        super().__init__(name="ProductsPackagerAgent", role="Distribution")
        self.db = db
        self.load_skill("bundle_creation")
        self.load_skill("metadata_management")
        self.load_skill("quality_verification")

    def run(self, task_context: Dict[str, Any]) -> Any:
        # Access results from previous steps in the workflow
        product_info = task_context.get("create_product", {})
        package_name = task_context.get("package_name", "product_bundle")
        
        self.log(f"Packaging product: {package_name}")
        
        # Placeholder: Simulated packaging logic
        package_result = {
            "package_name": package_name,
            "status": "packaged",
            "files_included": [product_info.get("download_url", "unknown_url")],
            "metadata": {"version": "1.0", "created_at": "2026-09-12"}
        }
        
        self.db.write_airtable("product_packages", package_result)
        return package_result
