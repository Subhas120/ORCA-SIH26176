"""
ORCA Agent Orchestrator

Coordinates specialized ORCA agents according to the execution
plan produced by the Planner.
"""

from agents.intent.intent_extractor import analyze_query
from agents.planner.planner import create_plan
from agents.common.agent_contract import AgentRequest, AgentResponse
from agents.context.context_manager import ConversationContext
from agents.validation.query_validator import (
    validate_query,
    get_clarification_message,
)
from agents.orchestrator.response_aggregator import aggregate_responses
from agents.orchestrator.parallel_executor import execute_agents_sync


def build_execution_context(
    query: str,
    context: ConversationContext | None = None,
) -> dict:
    """
    Convert a natural-language query into an ORCA execution context.

    Missing entities are filled from conversation context when
    a context object is supplied.
    """

    analysis = analyze_query(query)

    entities = {
        "location": analysis["location"],
        "date": analysis["date"],
        "time": analysis["time"],
        "activity": analysis["activity"],
    }

    if context is not None:
        entities = context.fill_missing(entities)

    plan = create_plan(analysis["intent"])

    return {
        "query": query,
        "intent": analysis["intent"],
        "entities": entities,
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


def create_agent_requests(
    execution_context: dict,
) -> list[AgentRequest]:
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
    handlers: dict | None = None,
    context: ConversationContext | None = None,
) -> dict:
    """
    Run the complete M1 coordination pipeline.

    Pipeline:
        Query
          -> Intent + Entities
          -> Context Resolution
          -> Validation
          -> Planner
          -> Agent Requests
          -> Parallel Agent Execution
          -> Response Aggregation

    Invalid queries return a clarification response and do not
    execute specialized agents.
    """

    execution_context = build_execution_context(
        query,
        context=context,
    )

    validation = validate_query(
        execution_context["intent"],
        execution_context["entities"],
    )

    if not validation["valid"]:
        return {
            "query": query,
            "intent": execution_context["intent"],
            "entities": execution_context["entities"],
            "agents": [],
            "parallel": False,
            "agent_requests": [],
            "responses": aggregate_responses([]),
            "validation": validation,
            "clarification": get_clarification_message(
                execution_context["intent"],
                validation["missing"],
            ),
        }

    if context is not None:
        context.update(execution_context["entities"])

    agent_requests = create_agent_requests(execution_context)

    if handlers is not None:
        responses = execute_agents_sync(
            agent_requests=agent_requests,
            agent_names=execution_context["agents"],
            handlers=handlers,
        )

    elif responses is None:
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
        "validation": validation,
        "clarification": None,
    }


if __name__ == "__main__":
    query = "Is it safe to fish tomorrow near Kochi?"

    result = run_query(query)

    print("ORCA Execution Result:")
    print(result)
