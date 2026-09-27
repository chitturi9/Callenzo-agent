#!/usr/bin/env python3
"""Run a Callenzo supervisor job from the command line."""

import argparse
import json
import uuid


def main() -> None:
    parser = argparse.ArgumentParser(description="Callenzo multi-agent supervisor")
    parser.add_argument("goal", nargs="?", default="Design the self-hosted voice agent platform")
    parser.add_argument("--thread", default=None, help="Resume a memory thread id")
    args = parser.parse_args()
    thread_id = args.thread or str(uuid.uuid4())

    try:
        from .supervisor import build_graph

        app = build_graph()
        initial = {
            "messages": [{"role": "user", "content": args.goal}],
            "goal": args.goal,
            "plan": [],
            "active_agent": "chief_of_staff",
            "cycle": 0,
            "artifacts": [],
            "risks": [],
            "needs_human_approval": False,
            "approval_reason": None,
            "last_result": None,
            "memory_notes": [],
            "reviewed": False,
        }
        final = app.invoke(
            initial,
            config={"recursion_limit": 25, "configurable": {"thread_id": thread_id}},
        )
        engine = "langgraph"
    except Exception:
        from .runtime import run

        final = run(args.goal)
        engine = "builtin"

    print(
        json.dumps(
            {
                "engine": engine,
                "thread_id": thread_id,
                "goal": final.get("goal"),
                "active_agent": final.get("active_agent"),
                "cycle": final.get("cycle"),
                "reviewed": final.get("reviewed"),
                "needs_human_approval": final.get("needs_human_approval"),
                "approval_reason": final.get("approval_reason"),
                "plan": final.get("plan"),
                "risks": final.get("risks"),
                "artifacts": final.get("artifacts"),
                "memory_notes": final.get("memory_notes"),
                "last_result": final.get("last_result"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
