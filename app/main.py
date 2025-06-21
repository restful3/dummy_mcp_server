from mcp.server.fastmcp import FastMCP, Context

from app.tools.echo import echo
from app.tools.dummy import dummy

mcp = FastMCP(
    "Dummy MCP Server",
    description="FastMCP 1.0.0 with SSE, echo tool, and dummy tool.",
    host="0.0.0.0",
    port=8002
)

mcp.tool()(echo)
mcp.tool()(dummy)

if __name__ == "__main__":
    print("FastMCP 1.0.0 + SSE 테스트 서버 시작2 (Target Port: 8002)", flush=True)
    try:
        mcp.run(transport="sse")
    except Exception as e:
        print(f"서버 실행 중 오류 발생: {e}", flush=True) 