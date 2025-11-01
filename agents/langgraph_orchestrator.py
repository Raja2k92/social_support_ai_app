from langgraph.graph import StateGraph, START, END

from agents.data_extraction_agent import DataExtractionAgent
from agents.data_validation_agent import DataValidationAgent
from agents.decision_agent import DecisionAgent
from agents.eligibility_agent import EligibilityAgent
from core.state_schema import AppState


def run_orchestrator(attachments):
    extraction_agent = DataExtractionAgent()
    validation_agent = DataValidationAgent()
    eligibility_agent = EligibilityAgent()
    decision_agent = DecisionAgent()

    builder = StateGraph(AppState)

    # Each node must return a dict with at least one key from AppState
    builder.add_node(
        "extract",
        lambda state: {"extracted_data": extraction_agent.process(state["attachments"])}
    )

    builder.add_node(
        "validate",
        lambda state: {"validation": validation_agent.process(state["extracted_data"])}
    )

    builder.add_node(
        "assess",
        lambda state: {"eligibility": eligibility_agent.assess(state["extracted_data"])}
    )

    builder.add_node(
        "decide",
        lambda state: {"decision": decision_agent.make_decision(state["validation"], state["eligibility"],
                                                                state["extracted_data"])}
    )

    builder.add_edge(START, "extract")
    builder.add_edge("extract", "validate")
    builder.add_edge("validate", "assess")
    builder.add_edge("assess", "decide")
    builder.add_edge("decide", END)

    graph = builder.compile()
    results = graph.invoke({"attachments": attachments})

    return results
