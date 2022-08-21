from fastapi import WebSocket, status, Query
from typing import Optional
from ..redis.config import Redis

# To be able to distinguish between two different client sessions 
# and limit the chat sessions, use a timed token, 
# passed as a query parameter to the WebSocket connection
async def get_token(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):

    if token is None or token == "":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    redis = Redis()
    redis_client = await redis.create_connection()
    isexists = await redis_client.exists(token)

    if isexists == 1:
        return token
    else:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Session not authenticated or expired token")