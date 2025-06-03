from mcp.server.fastmcp import Context
# StreamingResponse는 더 이상 직접 사용하지 않으므로 주석 처리하거나 삭제 가능
# from fastapi.responses import StreamingResponse 
import asyncio # 비동기 작업을 위해 추가

async def echo(ctx: Context, message: str):
    """
    입력받은 메시지를 3회 반복하여 스트리밍으로 반환합니다.
    각 메시지 사이에는 1초의 지연이 있습니다.
    """
    for i in range(3):
        message_content = f"{message} ({i+1}/3)"
        try:
            await ctx.stream_result_chunk(message_content)
        except Exception as e:
            print(f"DEBUG: 스트리밍 중 오류 발생: {e}", flush=True)
            break # 오류 발생 시 루프 중단
        await asyncio.sleep(1)
    
    return {"status": "Echo stream completed"}

# StreamingResponse를 반환하는 이전 로직은 제거됩니다. 