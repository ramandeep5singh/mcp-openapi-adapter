import os
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
from dotenv import load_dotenv

load_dotenv()

with open("servers.json") as f:
    MCP_SERVERS = json.load(f)

app = FastAPI()

# MCP SERVER REGISTRY ---------->

# MCP_SERVERS = {
#     "expense": {
#         "url": "https://ai-expense-tracker-mcp-server.fastmcp.app/mcp",
#         "token": os.getenv("MCP_EXPENSE_TOKEN")
#     }
# }

#TOOL SERVER MAPPING ---------->

TOOL_MAP = {
    #Expense MCP Tools
    "summary": "expense",
    "get_expenses": "expense",
    "total_expenses": "expense",
    "add_expense": "expense",
    "delete_expense": "expense",
    "range_expenses": "expense"


}

# MCP_URL = "https://ai-expense-tracker-mcp-server.fastmcp.app/mcp"
# TOKEN = "fmcp_-SVzWwg9HrzicCeEy4m4XioKe6JHFfV9U-ROVuOsyDw"

# def call_tool(tool, args):
#     headers = {
#         "Authorization": f"Bearer {TOKEN}",
#         "Content-Type": "application/json",
#         "Accept": "application/json, text/event-stream"
#     }

#     payload = {
#         "jsonrpc": "2.0",
#         "id": "1",
#         "method": "tools/call",
#         "params": {
#             "name": tool,
#             "arguments": args
#         }
#     }

#     print("Sending to MCP:", payload)

#     r = requests.post(MCP_URL, headers=headers, json=payload)

#     print("MCP RESPONSE:", r.text)

#     text = r.text

#     # extract JSON from SSE format
#     if "data:" in text:
#         json_part = text.split("data:")[1].strip()
#         result = json.loads(json_part)

#         return {
#             "message": result["result"]["content"][0]["text"]
#         }

#     return {"error": "Invalid MCP response"}

class ToolRequest(BaseModel):
    tool: str
    arguments: dict = {}


def call_tool(tool, args):

    server_name = TOOL_MAP.get(tool)

    if not server_name:
        return {"error": f"Tool '{tool}' not registered"}

    server = MCP_SERVERS.get(server_name)

    if not server:
        return {"error": f"MCP server '{server_name}' not configured"}
    
    token = os.getenv(server["token_env"])

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }

    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/call",
        "params": {
            "name": tool,
            "arguments": args
        }
    }

    response = requests.post(
        server["url"],
        headers=headers,
        json=payload,
        stream=True,
        timeout=30
    )

    response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue

        decoded = line.decode("utf-8")

        if decoded.startswith("data:"):
            json_data = decoded[5:].strip()

            try:
                return json.loads(json_data)
            except json.JSONDecodeError:
                continue

    return {"error": "No response from MCP server"}


# TOOL API ENDPOINTS ---------->


@app.get("/summary")
def summary():
    return call_tool("summary", {})


@app.get("/expenses")
def get_expenses():
    return call_tool("get_expenses", {})


@app.get("/total_expenses")
def total_expenses():
    return call_tool("total_expenses", {})


@app.post("/add_expense")
def add_expense(date: str, amount: float, category: str, subcategory: str, note: str):
    return call_tool(
        "add_expense",
        {
            "date": date,
            "amount": amount,
            "category": category,
            "subcategory": subcategory,
            "note": note
        }
    )


@app.delete("/delete_expense")
def delete_expense(expense_id: int):
    return call_tool(
        "delete_expense",
        {
            "expense_id": expense_id
        }
    )


@app.get("/range_expenses")
def range_expenses(start_date: str, end_date: str):
    return call_tool(
        "range_expenses",
        {
            "start_date": start_date,
            "end_date": end_date
        }
    )

#Generic RPC Gateway endpoint for any tool
@app.post("/call_tool") 
def call_tool_endpoint(request: ToolRequest):
    return call_tool(request.tool, request.arguments)

#discover tools automatically from TOOL_MAP
@app.get("/tools")
def list_tools():
    tools = []

    for tool, server in TOOL_MAP.items():
        tools.append({
            "name": tool,
            "server": server
        })

    return {"tools": tools}