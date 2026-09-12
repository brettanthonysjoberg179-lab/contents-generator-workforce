from typing import Any, Dict, List

# Define example workflows
WORKFLOWS = {
    "trend_research": [
        {"step_name": "discover_trends", "agent_id": "trend_agent", "input_key": None},
        {"step_name": "research_topic", "agent_id": "research_agent", "input_key": "topic"}
    ],
    "ebook_market_research": [
        {"step_name": "market_analysis", "agent_id": "ebook_research_agent", "input_key": "niche"}
    ],
    "seo_optimization": [
        {"step_name": "seo_analysis", "agent_id": "seo_research_agent", "input_key": "topic"}
    ],
    "content_creation": [
        {"step_name": "generate_copy", "agent_id": "copywriting_agent", "input_key": "topic"}
    ],
    "article_production": [
        {"step_name": "draft_content", "agent_id": "writer_agent", "input_key": "topic"},
        {"step_name": "assemble_page", "agent_id": "pageonator_agent", "input_key": None}
    ],
    "content_publishing": [
        {"step_name": "draft_content", "agent_id": "writer_agent", "input_key": "topic"},
        {"step_name": "assemble_page", "agent_id": "pageonator_agent", "input_key": None},
        {"step_name": "publish_content", "agent_id": "publisher_agent", "input_key": "platform"}
    ],
    "ebook_production": [
        {"step_name": "design_cover", "agent_id": "cover_designer_agent", "input_key": "topic"},
        {"step_name": "draft_content", "agent_id": "writer_agent", "input_key": "topic"},
        {"step_name": "assemble_page", "agent_id": "pageonator_agent", "input_key": None}
    ],
    "product_sale": [
        {"step_name": "process_payment", "agent_id": "sales_agent", "input_key": None}
    ],
    "product_fulfillment": [
        {"step_name": "process_payment", "agent_id": "sales_agent", "input_key": None},
        {"step_name": "deliver_product", "agent_id": "fulfillment_agent", "input_key": None}
    ],
    "business_review": [
        {"step_name": "generate_report", "agent_id": "business_manager_agent", "input_key": "report_type"}
    ],
    "financial_audit": [
        {"step_name": "run_analysis", "agent_id": "financial_adviser_agent", "input_key": "analysis_type"}
    ],
    "strategic_planning": [
        {"step_name": "create_roadmap", "agent_id": "business_planner_agent", "input_key": "goal"}
    ],
    "business_automation": [
        {"step_name": "run_automation", "agent_id": "business_automation_agent", "input_key": "automation_task"}
    ],
    "workflow_planning": [
        {"step_name": "design_workflow", "agent_id": "workflow_planner_agent", "input_key": "goal"}
    ],
    "digital_product_creation": [
        {"step_name": "assemble_page", "agent_id": "pageonator_agent", "input_key": None},
        {"step_name": "create_product", "agent_id": "digital_product_creator_agent", "input_key": "format"}
    ],
    "product_packaging": [
        {"step_name": "assemble_page", "agent_id": "pageonator_agent", "input_key": None},
        {"step_name": "create_product", "agent_id": "digital_product_creator_agent", "input_key": "format"},
        {"step_name": "package_product", "agent_id": "products_packager_agent", "input_key": None}
    ],
    "product_ideation": [
        {"step_name": "generate_concept", "agent_id": "digital_product_concept_agent", "input_key": "topic"}
    ]
}

def get_workflow(workflow_id: str) -> List[Dict[str, Any]]:
    return WORKFLOWS.get(workflow_id, [])
