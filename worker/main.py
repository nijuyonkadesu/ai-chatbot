from src.redis.config import Redis
from src.redis.cache import Cache
import asyncio

# Test reddis connection
async def main():
    redis = Redis()
    json_client = redis.create_rejson_connection()

    # append new message into Redis
    await Cache(json_client).add_message_to_cache(token="0b001ee4-2e0c-466f-a63b-8b57225b4a34", message_data={
        "id": "1",
        "msg": "what are you and why are you?",
        "timestamp": "2022-08-21 09:21:50.092109"
    })

    # get chat history of the respective person
    data = await Cache(json_client).get_chat_history(token="0b001ee4-2e0c-466f-a63b-8b57225b4a34")
    print(data)
    
if __name__ == "__main__":
    asyncio.run(main())