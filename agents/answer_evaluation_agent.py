from config import llm
from graph.state import AgentState
from models.schemas import EvaluationResult
from prompts.evaluation import EVALUATION_PROMPT


def answer_evaluation_agent(state: AgentState) -> AgentState:
    structured_llm = llm.with_structured_output(EvaluationResult)

    result = structured_llm.invoke(
        EVALUATION_PROMPT.format(
            query=state["query"],
            answer=state["answer"],
        )
    )

    state["evaluation_passed"] = result.passed
    state["evaluation_feedback"] = result.feedback

    return state
