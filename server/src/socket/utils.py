from fastapi import WebSocket, status, Query
from typing import Optional

# To be able to distinguish between two different client sessions 
# and limit the chat sessions, use a timed token, 
# passed as a query parameter to the WebSocket connection
async def get_token(
    websocket: WebSocket,
    token: Optional[str] = Query(None)
):
    if token is None or token == "":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return token