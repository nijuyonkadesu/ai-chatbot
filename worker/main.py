from src.redis.config import Redis
from src.redis.cache import Cache
import asyncio
from src.model.gptj import GPT
from src.scheme.chat import Message
from src.redis.stream import StreamConsumer
from src.redis.producer import Producer

redis = Redis()


async def main():
    # Test reddis connection - Message Queue
    json_client = redis.create_rejson_connection()
    redis_client = await redis.create_connection()
    consumer = StreamConsumer(redis_client)
    cache = Cache(json_client)
    producer = Producer(redis_client)

    print("Stream consumer started")
    print("Stream waiting for new messages")

    while True:
        response = await consumer.consume_stream(
                stream_channel="message_channel", count=1, block=0)

        if response:
            for stream, messages in response:
                # Get message from stream,
                # and extract token, message data and message id
                for message in messages:
                    message_id = message[0]
                    token = [k.decode('utf-8')
                             for k, v in message[1].items()][0]
                    message = [v.decode('utf-8')
                               for k, v in message[1].items()][0]

                    # Create a new message instance
                    # and add to cache, specifying the source as human
                    msg = Message(msg=message)

                    await cache.add_message_to_cache(
                            token=token,
                            source="human",
                            message_data=msg.dict())

                    # Get chat history from cache
                    data = await cache.get_chat_history(token=token)

                    # Clean message input and send to query
                    # Take past 4 messages from the whole chat history
                    message_data = data['messages'][-4:]

                    input = ["" + i['msg'] for i in message_data]
                    input = " ".join(input)

                    res = GPT().query(input=input)

                    msg = Message(
                        msg=res
                    )

                    # responses from the GPT is added
                    # to response_channel with token as key
                    stream_data = {}
                    stream_data[str(token)] = str(msg.dict())

                    await producer.add_to_stream(stream_data,
                                                 "response_channel")

                    # adding GPT's response to the requested uuid (user)
                    await cache.add_message_to_cache(token=token,
                                                     source="bot",
                                                     message_data=msg.dict())

                # Delete messaage from msg queue after it has been processed
                await consumer.delete_message(stream_channel="message_channel",
                                              message_id=message_id)


if __name__ == "__main__":
    asyncio.run(main())

# Since this is a worker, it has a separate
# main function.
# this has to be run along with server main
