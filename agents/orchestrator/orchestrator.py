"""
ORCA Agent Orchestrator

Coordinates specialized ORCA agents according to the execution
plan produced by the Planner.
"""

from agents.intent.intent_extractor import analyze_query
from agents.planner.planner import create_plan
from agents.common.agent_contract import AgentRequest, AgentResponse
from agents.orchestrator.response_aggregator import aggregate_responses


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
    """

    tasks = []

    for agent in execution_context["agents"]:
        tasks.append({
            "agent": agent,
            "query": execution_context["query"],
            "entities": execution_context["entities"].copy(),
        })

    return tasks


def create_agent_requests(execution_context: dict) -> list[AgentRequest]:
    """
    Convert an execution context into standardized AgentRequest objects.
    """

    requests = []

    entities = execution_context["entities"]

    for agent in execution_context["agents"]:
        requests.append(
            AgentRequest(
                query=execution_context["query"],
                location=entities["location"],
                date=entities["date"],
                time=entities["time"],
                activity=entities["activity"],
            )
        )

    return requests


def run_query(
    query: str,
    responses: list[AgentResponse] | None = None,
) -> dict:
    """
    Run the M1 coordination pipeline.

    Pipeline:
        Query
          -> Intent + Entities
          -> Planner
          -> Agent Requests
          -> Response Aggregation

    Specialized-agent execution remains outside M1 so that
    M2/M3/M4/M5 can provide their own implementations.
    """

    execution_context = build_execution_context(query)

    agent_requests = create_agent_requests(execution_context)

    if responses is None:
        responses = []

    aggregated = aggregate_responses(responses)

    return {
        "query": query,
        "intent": execution_context["intent"],
        "entities": execution_context["entities"],
        "agents": execution_context["agents"],
        "parallel": execution_context["parallel"],
        "agent_requests": agent_requests,
        "responses": aggregated,
    }


if __name__ == "__main__":
    query = "Is it safe to fish tomorrow near Kochi?"

    result = run_query(query)

    print("ORCA Execution Result:")
    print(result)
