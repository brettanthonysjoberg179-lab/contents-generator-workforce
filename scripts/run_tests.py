#!/usr/bin/env python3
"""Run all tests for the Content Generator Workforce."""
import subprocess
import sys

def main():
    print("Running Content Generator Workforce tests...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd=str(Path(__file__).parent.parent)
    )
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()