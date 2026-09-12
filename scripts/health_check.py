#!/usr/bin/env python3
"""Check system health for the Content Generator Workforce."""
import os
import sys
import json
from pathlib import Path

def check_ollama():
    """Check if Ollama is running."""
    try:
        import urllib.request
        resp = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5)
        data = json.loads(resp.read())
        models = [m["name"] for m in data.get("models", [])]
        return {"status": "healthy", "models": models}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def check_env():
    """Check environment variables."""
    required = ["COMPOSIO_API_KEY", "OLLAMA_BASE_URL"]
    missing = [v for v in required if not os.getenv(v)]
    return {"status": "ok" if not missing else "missing", "missing": missing}

def check_project():
    """Check project structure."""
    root = Path(__file__).parent.parent
    required_files = [
        "pyproject.toml", "run_workforce.py", "shared/base_agent.py",
        "agents/orchestrator/agent.py", "mcp_server/main.py", "config/workforce.yaml"
    ]
    missing = [f for f in required_files if not (root / f).exists()]
    return {"status": "ok" if not missing else "missing", "missing": missing}

def main():
    print("Content Generator Workforce - Health Check")
    print("=" * 50)
    
    checks = {
        "ollama": check_ollama(),
        "environment": check_env(),
        "project": check_project(),
    }
    
    for name, result in checks.items():
        status = result["status"]
        icon = "✓" if status == "ok" or status == "healthy" else "✗"
        print(f"\n{icon} {name}: {status}")
        if "models" in result:
            print(f"  Models: {', '.join(result['models'])}")
        if "missing" in result and result["missing"]:
            print(f"  Missing: {', '.join(result['missing'])}")
    
    all_ok = all(r["status"] in ("ok", "healthy") for r in checks.values())
    print(f"\n{'=' * 50}")
    print(f"All systems {'healthy' if all_ok else 'issues detected'}.")
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())