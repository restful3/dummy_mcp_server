from mcp.server.fastmcp import Context

# --- 아주 간단한 더미 툴 정의 ---
def dummy(ctx: Context, message: str) -> dict:
    print(f"SYNC_DEBUG_dummy: dummy called with message: {message}", flush=True)
    return {
        "tool_name": "dummy",
        "execution_status": "success",
        "details": f"Dummy tool processed message: {message}"
    } 