from langgraph.graph import StateGraph

from state import ChatState

from nodes.input_node import input_node
from nodes.intent_node import intent_node
from nodes.response_node import response_node


builder = StateGraph(ChatState)

builder.add_node(
    "input",
    input_node
)

builder.add_node(
    "intent",
    intent_node
)

builder.add_node(
    "response",
    response_node
)

builder.set_entry_point("input")

builder.add_edge(
    "input",
    "intent"
)

builder.add_edge(
    "intent",
    "response"
)

graph = builder.compile()