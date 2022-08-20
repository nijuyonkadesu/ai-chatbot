from src.redis.config import Redis
import asyncio

# Test reddis connection
async def main():
    redis = Redis()
    redis = await redis.create_connection()
    print(redis)
    await redis.set("hana", "bira")

if __name__ == "__main__":
    asyncio.run(main())
