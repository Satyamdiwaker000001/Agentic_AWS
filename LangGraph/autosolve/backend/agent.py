import operator
from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

# --- Define State ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    department: str
    escalated: bool

# --- Tools ---
@tool
def get_invoice_details(invoice_id: str) -> str:
    """Gets details for an invoice."""
    return f"Invoice {invoice_id} is for $150. Status: Paid."

@tool
def process_refund(invoice_id: str, amount: float) -> str:
    """Processes a refund. Amounts over $100 require escalation."""
    if amount > 100:
        return "ESCALATION_REQUIRED: Amount exceeds auto-approval limit."
    return f"Successfully refunded ${amount} for invoice {invoice_id}."

tools = [get_invoice_details, process_refund]
tool_node = ToolNode(tools)

# --- Nodes ---
# Initialize LLM (Requires OPENAI_API_KEY in environment)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def triage_node(state: AgentState):
    """Routes the conversation to the right department based on user query."""
    messages = state['messages']
    
    # System prompt for triage
    sys_msg = (
        "You are a triage agent. Analyze the user's request and classify the department as 'billing' or 'general'. "
        "Output ONLY the word 'billing' or 'general'."
    )
    
    response = llm.invoke([{"role": "system", "content": sys_msg}] + messages)
    department = response.content.strip().lower()
    
    # Fallback
    if department not in ["billing", "general"]:
        department = "general"
        
    return {"department": department}

def billing_node(state: AgentState):
    """Handles billing queries using tools."""
    messages = state['messages']
    llm_with_tools = llm.bind_tools(tools)
    
    sys_msg = (
        "You are a helpful billing agent. You can look up invoices and process refunds. "
        "If a tool returns 'ESCALATION_REQUIRED', you must reply that the request has been forwarded to a human manager for approval."
    )
    
    response = llm_with_tools.invoke([{"role": "system", "content": sys_msg}] + messages)
    
    # Check if the tool returned an escalation requirement (simplified check)
    escalated = False
    if "ESCALATION_REQUIRED" in response.content or (isinstance(response, AIMessage) and response.tool_calls):
        # We will handle the actual escalation logic via conditional edges or state checks
        pass
        
    return {"messages": [response]}

def general_node(state: AgentState):
    """Handles general support queries."""
    messages = state['messages']
    sys_msg = "You are a helpful customer support agent. Answer the user's query politely."
    response = llm.invoke([{"role": "system", "content": sys_msg}] + messages)
    return {"messages": [response]}

def escalation_node(state: AgentState):
    """This node represents human-in-the-loop. The graph will interrupt BEFORE this node."""
    messages = state['messages']
    # Once human approves, this node executes
    approval_msg = AIMessage(content="Manager has approved the escalation. Proceeding with refund.")
    return {"messages": [approval_msg], "escalated": False}

# --- Routing Logic ---
def route_after_triage(state: AgentState) -> str:
    if state.get("department") == "billing":
        return "billing"
    return "general"

def route_after_billing(state: AgentState) -> Literal["tools", "escalation", "__end__"]:
    last_msg = state['messages'][-1]
    if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
        # Check if the tool call is for a refund > $100
        for tc in last_msg.tool_calls:
            if tc['name'] == 'process_refund' and tc['args'].get('amount', 0) > 100:
                return "escalation"
        return "tools"
    return "__end__"

# --- Build Graph ---
builder = StateGraph(AgentState)

builder.add_node("triage", triage_node)
builder.add_node("billing", billing_node)
builder.add_node("general", general_node)
builder.add_node("tools", tool_node)
builder.add_node("escalation", escalation_node)

builder.set_entry_point("triage")

# Triage routing
builder.add_conditional_edges("triage", route_after_triage)

# Billing routing
builder.add_conditional_edges("billing", route_after_billing)

# Tools return back to billing
builder.add_edge("tools", "billing")

# Escalation edge
builder.add_edge("escalation", "billing")
builder.add_edge("general", END)

# Compile graph with interrupt before escalation node (HITL)
# We will pass a checkpointer from the server
def compile_graph(checkpointer):
    return builder.compile(
        checkpointer=checkpointer, 
        interrupt_before=["escalation"]
    )
