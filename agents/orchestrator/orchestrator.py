"""
ORCA Agent Orchestrator

Coordinates specialized ORCA agents according to the execution
plan produced by the Planner.
"""

from agents.intent.intent_extractor import analyze_query
from agents.planner.planner import create_plan


def build_execution_context(query: str) -> dict:
    """
    Convert a natural-language query into an ORCA execution context.

    Pipeline:
        Query -> Intent + Entities -> Planner -> Execution Context
    """

    analysis = analyze_query(query)

    plan = create_plan(analysis["intent"])

    return {
        "query": query,
        "intent": analysis["intent"],
        "entities": {
            "location": analysis["location"],
            "date": analysis["date"],
            "time": analysis["time"],
            "activity": analysis["activity"],
        },
        "agents": plan["agents"],
        "parallel": plan["parallel"],
    }


def get_agent_tasks(execution_context: dict) -> list:
    """
    Convert an execution context into independent agent tasks.

    Each task contains the same user context and identifies the
    specialized agent responsible for producing that part of the
    response.
    """

    tasks = []

    for agent in execution_context["agents"]:
        tasks.append({
            "agent": agent,
            "query": execution_context["query"],
            "entities": execution_context["entities"].copy(),
        })

    return tasks


if __name__ == "__main__":
    query = "Is it safe to fish tomorrow near Kochi?"

    context = build_execution_context(query)

    print("Execution Context:")
    print(context)

    print("\nAgent Tasks:")
    for task in get_agent_tasks(context):
        print(task)
