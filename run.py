"""
run.py

Runs the complete SaaS API Research Agent pipeline.

Pipeline:
1. Research Agent
2. Verification
3. Insights Generation

Author: Pavan Kumar
"""

import subprocess
import sys


def run_script(script):
    print(f"\n{'=' * 60}")
    print(f"Running: {script}")
    print(f"{'=' * 60}")

    result = subprocess.run([sys.executable, script])

    if result.returncode != 0:
        print(f"\n❌ Error while running {script}")
        sys.exit(result.returncode)

    print(f"✅ Completed: {script}")


def main():
    print("\n🚀 Starting SaaS API Research Agent\n")

    run_script("agent/research_agent.py")
    run_script("agent/verify.py")
    run_script("agent/insights.py")

    print("\n" + "=" * 60)
    print("🎉 Pipeline completed successfully!")
    print("=" * 60)
    print("\nGenerated files:")
    print("✔ output/research.csv")
    print("✔ output/verified.csv")
    print("✔ output/insights.json")
    print("\nOpen html/index.html to view the dashboard.")


if __name__ == "__main__":
    main()