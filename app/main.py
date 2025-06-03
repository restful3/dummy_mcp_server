print("DEBUG: main.py execution started", flush=True)
from mcp.server.fastmcp import FastMCP, Context

print("DEBUG: Imports in main.py finished", flush=True)

from app.tools.echo import echo
from app.tools.dummy import dummy

print("DEBUG: Tool imports in main.py finished", flush=True)

mcp = FastMCP(
    "Dummy MCP Server",
    description="FastMCP 1.0.0 with SSE, echo tool, and dummy tool.",
    host="0.0.0.0",
    port=8002
)

print(f"DEBUG: FastMCP object created: {mcp}", flush=True)

print(f"--- Registering echo tool ---", flush=True)
mcp.tool()(echo)
print(f"--- echo tool registered ---", flush=True)

print(f"--- Registering dummy tool ---", flush=True)
mcp.tool()(dummy)
print(f"--- dummy tool registered ---", flush=True)

if __name__ == "__main__":
    print("DEBUG: Entering __main__ block", flush=True)
    print("FastMCP 1.0.0 + SSE 테스트 서버 시작 (Target Port: 8002)", flush=True)
    
    try:
        print(f"DEBUG: About to call mcp.run(transport='sse') using constructor host/port", flush=True)
        mcp.run(transport="sse")
    except Exception as e:
        print(f"An unexpected error occurred during mcp.run(): {e}", flush=True) 