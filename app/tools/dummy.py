from mcp.server.fastmcp import Context

# --- 아주 간단한 더미 툴 정의 ---
def dummy(ctx: Context, message: str) -> dict:
    return {
        "tool_name": "dummy",
        "execution_status": "success",
        "details": "안녕하세요 반가워요"
    } 