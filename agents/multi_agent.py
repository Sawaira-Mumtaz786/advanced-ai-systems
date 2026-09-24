import os
import json
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-20b"

class AgentState(TypedDict):
    raw_input: str
    structured_data: dict
    validation_status: str
    final_action: str
    human_approved: bool

def agent_a_structured(state: AgentState) -> AgentState:
    prompt = f"""Convert this raw input into JSON with keys: name, amount, category.
Input: {state['raw_input']}
Respond ONLY with valid JSON. Nothing else."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    try:
        structured = json.loads(response.choices[0].message.content.strip())
    except:
        structured = {"name": "unknown", "amount": 0, "category": "unknown"}
    return {**state, "structured_data": structured}

def agent_b_evaluator(state: AgentState) -> AgentState:
    data = state["structured_data"]
    amount = data.get("amount", 0)
    status = "needs_human_approval" if amount > 1000 else "auto_approved"
    return {**state, "validation_status": status}

def route_after_b(state: AgentState) -> Literal["human_checkpoint", "finalize"]:
    return "human_checkpoint" if state["validation_status"] == "needs_human_approval" else "finalize"

def human_checkpoint(state: AgentState) -> AgentState:
    return {**state, "final_action": "pending_human_approval"}

def finalize(state: AgentState) -> AgentState:
    return {**state, "final_action": "approved_and_executed"}

workflow = StateGraph(AgentState)
workflow.add_node("agent_a", agent_a_structured)
workflow.add_node("agent_b", agent_b_evaluator)
workflow.add_node("human_checkpoint", human_checkpoint)
workflow.add_node("finalize", finalize)

workflow.set_entry_point("agent_a")
workflow.add_edge("agent_a", "agent_b")
workflow.add_conditional_edges("agent_b", route_after_b)
workflow.add_edge("human_checkpoint", END)
workflow.add_edge("finalize", END)

graph = workflow.compile()

def run_agent(raw_input: str):
    return graph.invoke({
        "raw_input": raw_input,
        "structured_data": {},
        "validation_status": "",
        "final_action": "",
        "human_approved": False,
    })

if __name__ == "__main__":
    print(run_agent("Customer Ahmed paid 5000 dollars for premium plan"))
