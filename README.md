# MCP FastAPI Adapter

This project is a lightweight FastAPI adapter that allows a local AI client (like OpenWebUI) to communicate with remote MCP servers.

It acts as a bridge between an AI interface and MCP tools, enabling natural language commands to trigger backend tool execution.

---

## Architecture

AI Client (OpenWebUI / LLM)
        ↓
FastAPI MCP Adapter
        ↓
Remote MCP Server
        ↓
Database / External Services

---

## Features

- Connects AI clients to remote MCP servers
- Routes tool calls through FastAPI endpoints
- Supports multiple MCP servers via server registry
- Handles MCP streaming responses (SSE)
- Simple tool → server mapping system

---

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Requests
- MCP (Model Context Protocol)

---

## Project Structure

```
mcp-openapi-adapter
│
├── server.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

Clone the repository

```
git clone https://github.com/ramandeep5singh/mcp-openapi-adapter.git
cd mcp-openapi-adapter
```

Install dependencies

```
pip install -r requirements.txt
```

Run the adapter

```
uvicorn server:app --reload --port 9000
```

---

## Example Endpoints

```
GET /summary
GET /expenses
GET /total_expenses
POST /add_expense
DELETE /delete_expense
GET /range_expenses
```

---

## Future Improvements

- Generic `/call_tool` endpoint
- Automatic MCP tool discovery
- Multi-MCP server routing
- Production-ready logging and error handling

---

## Author

Built as part of an MCP learning project exploring how AI clients interact with tool servers using the Model Context Protocol.