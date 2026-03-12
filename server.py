import os
from fastapi import FastAPI
import requests
import json

app = FastAPI()

# MCP SERVER REGISTRY ---------->

MCP_SERVERS = {
    "expense": {
        "url": "https://ai-expense-tracker-mcp-server.fastmcp.app/mcp",
        "token": os.getenv("MCP_EXPENSE_TOKEN")
    }
}

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


def call_tool(tool, args):

    server_name = TOOL_MAP.get(tool)
    server = MCP_SERVERS.get(server_name)

    headers = {
        "Authorization": f"Bearer {server['token']}",
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

    # Parse SSE safely
    for line in response.iter_lines():
        if line:
            decoded = line.decode("utf-8")

            if decoded.startswith("data:"):
                json_data = decoded.replace("data:", "").strip()

                try:
                    import json
                    return json.loads(json_data)
                except:
                    return {"error": "Invalid MCP response"}

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