from langgraph.graph import StateGraph, END
from state import ChatState

from nodes.router_node import router_node
from routes.route_task import route_task

from agents.general_agent import general_agent
from agents.coding_agent import coding_agent
from agents.math_agent import math_agent
from agents.debug_agent import debug_agent
from agents.physics_agent import physics_agent

builder = StateGraph(ChatState)

# Register nodes
builder.add_node("router", router_node)
builder.add_node("general_agent", general_agent)
builder.add_node("coding_agent", coding_agent)
builder.add_node("math_agent", math_agent)
builder.add_node("debug_agent", debug_agent)
builder.add_node("physics_agent", physics_agent)

# Set entry point
builder.set_entry_point("router")

# Set conditional routing
builder.add_conditional_edges(
    "router",
    route_task,
    {
        "general": "general_agent",
        "coding": "coding_agent",
        "math": "math_agent",
        "debug": "debug_agent",
        "physics": "physics_agent"
    }
)

# Connect agents to the end of processing
builder.add_edge("general_agent", END)
builder.add_edge("coding_agent", END)
builder.add_edge("math_agent", END)
builder.add_edge("debug_agent", END)
builder.add_edge("physics_agent", END)

graph = builder.compile()