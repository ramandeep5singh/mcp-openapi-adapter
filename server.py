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

def discover_tools():
    tool_map = {}

    for name, server in MCP_SERVERS.items():

        token = os.getenv(server["token_env"])

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }

        payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "tools/list"
        }

        try:
            response = requests.post(
                server["url"],
                headers=headers,
                json=payload,
                stream=True
            )

            for line in response.iter_lines():

                if not line:
                    continue

                decoded = line.decode("utf-8")

                if decoded.startswith("data:"):

                    json_data = decoded.replace("data:", "").strip()
                    data = json.loads(json_data)

                    tools = data["result"]["tools"]

                    for tool in tools:
                        tool_map[tool["name"]] = name

                    break

        except Exception as e:
            print(f"Failed to discover tools from {name}: {e}")

    return tool_map

TOOL_MAP = discover_tools()

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