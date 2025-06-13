from mcp.server.fastmcp import Context

def echo(ctx: Context, message: str) -> dict:
    """
    입력받은 메시지를 그대로 반환합니다.
    """
    return {
        "tool_name": "echo",
        "execution_status": "success",
        "details": message
    } 