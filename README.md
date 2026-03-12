# MCP OpenAPI Adapter

A lightweight **FastAPI gateway that converts MCP (Model Context Protocol) tools into a standard REST/OpenAPI API** so that **any UI chatbot (OpenWebUI, custom apps, agents, etc.) can interact with MCP servers easily.**

This project acts as a **generic MCP client adapter** and **tool router**.

Instead of building custom integrations for every MCP server, this adapter exposes a simple REST API that forwards requests to MCP servers.

---

# Architecture

```
Chat UI (OpenWebUI / Agents / Apps)
            │
            │ REST API
            ▼
     MCP OpenAPI Adapter
       (FastAPI Gateway)
            │
            │ JSON-RPC (MCP)
            ▼
        MCP Servers
   (Expense Tracker, etc.)
```

The adapter:

• Discovers available tools from MCP servers  
• Routes tool calls automatically  
• Exposes them via a clean REST interface  

---

# Features

• Generic MCP client gateway  
• Supports multiple MCP servers  
• Tool auto-discovery (`/tools`)  
• Tool execution (`/call_tool`)  
• Config-driven architecture  
• Works with **OpenWebUI, Claude Desktop, or any AI client**  
• Environment variable support for secure tokens  
• FastAPI OpenAPI documentation automatically generated  

---

# Project Structure

```
mcp-openapi-adapter/
│
├── server.py          # FastAPI MCP adapter
├── servers.json       # MCP server registry
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variable template
└── README.md
```

---

# Installation

Clone the repository.

```
git clone https://github.com/ramandeep5singh/mcp-openapi-adapter.git
cd mcp-openapi-adapter
```

Create virtual environment.

```
python -m venv .venv
```

Activate environment.

Windows

```
.venv\Scripts\activate
```

Linux / Mac

```
source .venv/bin/activate
```

Install dependencies.

```
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

Example:

```
MCP_EXPENSE_TOKEN=your_mcp_api_token
```

Never commit real tokens to GitHub.

---

# Configure MCP Servers

Edit `servers.json`.

Example:

```
{
  "expense": {
    "url": "https://ai-expense-tracker-mcp-server.fastmcp.app/mcp",
    "token_env": "MCP_EXPENSE_TOKEN"
  }
}
```

You can add **multiple MCP servers**.

Example:

```
{
  "expense": {
    "url": "...",
    "token_env": "MCP_EXPENSE_TOKEN"
  },
  "calendar": {
    "url": "...",
    "token_env": "MCP_CALENDAR_TOKEN"
  }
}
```

---

# Run the Adapter

Start the FastAPI server.

```
uvicorn server:app --reload --port 9000
```

API documentation will be available at:

```
http://127.0.0.1:9000/docs
```

---

# API Endpoints

## Discover Tools

```
GET /tools
```

Returns all available MCP tools.

Example response:

```
{
  "tools": [
    {"name": "summary", "server": "expense"},
    {"name": "add_expense", "server": "expense"}
  ]
}
```

---

## Execute Tool

```
POST /call_tool
```

Request body:

```
{
  "tool": "add_expense",
  "arguments": {
    "date": "2026-03-12",
    "amount": 5,
    "category": "Food",
    "subcategory": "Coffee",
    "note": "Morning coffee"
  }
}
```

---

# Using with OpenWebUI

This adapter allows OpenWebUI to interact with MCP tools.

---

## Step 1 — Start OpenWebUI (Docker)

```
docker run -d \
-p 3000:8080 \
--name open-webui \
ghcr.io/open-webui/open-webui:main
```

Open:

```
http://localhost:3000
```

---

## Step 2 — Run MCP Adapter

Start the adapter locally.

```
uvicorn server:app --port 9000
```

Adapter endpoint:

```
http://host.docker.internal:9000
```

(`host.docker.internal` allows Docker containers to access the host machine.)

---

## Step 3 — Register API in OpenWebUI

Inside OpenWebUI:

```
Workspace
 → Tools
 → Add Tool
```

Use:

```
OpenAPI URL:
http://host.docker.internal:9000/openapi.json
```

OpenWebUI will automatically import:

```
GET /tools
POST /call_tool
```

---

## Step 4 — Use MCP Tools in Chat

The chatbot can now call MCP tools automatically.

Example prompts:

```
Show my expense summary
```

```
Add a new expense of 8 euros for shawarma
```

The AI will call `/call_tool` which forwards the request to the MCP server.

---

# Production Usage

For production deployments:

Recommended improvements:

• Run adapter behind **Nginx or reverse proxy**  
• Use **Docker container for the adapter**  
• Store tokens in **environment variables or secret manager**  
• Enable **logging and monitoring**  
• Configure **multiple MCP servers** for different capabilities  

---

# Example Use Cases

• AI personal assistants  
• Expense tracking AI agents  
• Developer copilots with tool access  
• Multi-tool LLM platforms  
• Custom AI SaaS applications  

---

# Tech Stack

• FastAPI  
• Python  
• Model Context Protocol (MCP)  
• OpenWebUI  
• Docker  

---

# Future Improvements

Planned enhancements:

• Automatic MCP tool discovery from servers  
• Tool caching and refresh endpoint  
• Logging and observability  
• Docker deployment support  
• Multi-server orchestration  
• Authentication layer for adapter API  

---

# Author

Ramandeep Singh

GitHub  
https://github.com/ramandeep5singh

---

# License

MIT License