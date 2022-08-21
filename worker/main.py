from src.redis.config import Redis
from src.redis.cache import Cache
import asyncio
from src.model.gptj import GPT
from src.scheme.chat import Message

# Test reddis connection - Message Queue
async def main():
    redis = Redis()
    json_client = redis.create_rejson_connection()

    # append new message into Redis
    await Cache(json_client).add_message_to_cache(token="da26403f-5565-41cd-ad11-efe38117a9ef", source="human", message_data={
        "id": "6",
        "msg": "hey hey, how long have you been workin?",
        "timestamp": "2022-08-21 09:47:50.092109"
    })

    # get chat history of the respective person
    data = await Cache(json_client).get_chat_history(token="da26403f-5565-41cd-ad11-efe38117a9ef")
    print(data)

    message_data = data['messages'][-4:]

    input = ["" + i['msg'] for i in message_data]
    input = " ".join(input)

    res = GPT().query(input=input)

    msg = Message(
        msg=res
    )

    print(msg)
    # Add Bot's response to json
    await Cache(json_client).add_message_to_cache(token="da26403f-5565-41cd-ad11-efe38117a9ef", source="bot", message_data=msg.dict())
    
if __name__ == "__main__":
    asyncio.run(main())