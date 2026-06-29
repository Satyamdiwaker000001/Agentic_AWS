import os
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# LangGraph dependencies
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

from agent import compile_graph

load_dotenv()

app = FastAPI(title="AutoSolve API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    thread_id: str
    message: str

class ApprovalRequest(BaseModel):
    thread_id: str
    approved: bool

# We will initialize the graph with an in-memory or SQLite checkpointer
graph = None
checkpointer = None

@app.on_event("startup")
async def startup_event():
    global graph, checkpointer
    checkpointer = AsyncSqliteSaver.from_conn_string("autosolve.db")
    await checkpointer.setup()
    graph = compile_graph(checkpointer)

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """Streams the graph execution events via Server-Sent Events (SSE)."""
    
    async def event_generator():
        config = {"configurable": {"thread_id": req.thread_id}}
        
        # Check if the graph is waiting for approval
        current_state = await graph.aget_state(config)
        if current_state and current_state.next and "escalation" in current_state.next:
            yield {"event": "error", "data": json.dumps({"error": "Waiting for human approval."})}
            return
            
        inputs = {"messages": [HumanMessage(content=req.message)]}
        
        async for event in graph.astream_events(inputs, config, version="v1"):
            kind = event["event"]
            
            # Stream specific useful events to the frontend
            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"].content
                if chunk:
                    yield {"event": "token", "data": json.dumps({"token": chunk})}
                    
            elif kind == "on_tool_start":
                yield {"event": "tool_start", "data": json.dumps({"tool": event['name'], "input": event['data'].get('input')})}
                
            elif kind == "on_tool_end":
                yield {"event": "tool_end", "data": json.dumps({"tool": event['name'], "output": str(event['data'].get('output'))})}
                
        # After execution, check if it paused
        final_state = await graph.aget_state(config)
        if final_state and final_state.next and "escalation" in final_state.next:
            yield {"event": "hitl_interrupt", "data": json.dumps({"status": "paused_for_approval", "message": "High-value refund detected. Escalated to Manager."})}
            
        yield {"event": "done", "data": "finished"}

    return EventSourceResponse(event_generator())

@app.get("/admin/pending")
async def get_pending_approvals():
    """Fetches threads that are paused waiting for human-in-the-loop."""
    # In a real app, we'd query the DB. For this demo, we can just check known thread states or mock it.
    # To properly fetch from checkpointer, we need thread IDs. 
    # For demo purposes, we will return a mock pending task if the DB doesn't have an easy API.
    # LangGraph checkpointing stores states by thread_id.
    
    # We will just expose the state if a client provides a thread_id
    pass

@app.post("/admin/approve")
async def approve_action(req: ApprovalRequest):
    """Resumes the graph execution after human approval or rejection."""
    config = {"configurable": {"thread_id": req.thread_id}}
    state = await graph.aget_state(config)
    
    if not state.next or "escalation" not in state.next:
        return {"error": "No pending escalation for this thread."}
        
    if req.approved:
        # Resume graph with nothing, it will execute the escalation node
        async for _ in graph.astream(None, config):
            pass
        return {"status": "approved_and_resumed"}
    else:
        # If rejected, we can inject a message and route back
        rejection = ToolMessage(content="Manager REJECTED the refund.", tool_call_id="manual")
        # Update state manually (complex in langgraph)
        # For simplicity, we just return a message to the user
        await graph.aupdate_state(config, {"messages": [AIMessage(content="I'm sorry, the manager has rejected the refund request.")]})
        return {"status": "rejected"}
