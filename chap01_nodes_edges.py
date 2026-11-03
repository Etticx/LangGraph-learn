"""Chapter 01 - State, nodes, edges. No LLM yet.

Run:  uv run chap01_nodes_edges.py
"""
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


# State = the dict that travels through the graph.
class State(TypedDict):
    text: str
    word_count: int
    summary: str


# Nodes = plain functions. They get the whole state, return only what they change.
def clean(state: State):
    print("clean   sees:", state)
    return {"text": state["text"].strip().lower()}


def count(state: State):
    print("count   sees:", state)
    return {"word_count": len(state["text"].split())}


def construct(state: State):
    print("construct sees:", state)
    return {"summary": f"'{state['text']}' has {state['word_count']} words"}


# Edges = arrows between nodes.
g = StateGraph(State)
g.add_node("clean", clean)
g.add_node("count", count)
g.add_node("construct", construct)
g.add_edge(START, "clean")
g.add_edge("clean", "count")
g.add_edge("count", "construct")
g.add_edge("construct", END)

app = g.compile()

if __name__ == "__main__":
    result = app.invoke({"text": "  Hello LangGraph World  "})
    print("final        :", result)
    print()
    print(app.get_graph().draw_mermaid())
