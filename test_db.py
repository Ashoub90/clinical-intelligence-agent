import asyncio
from app.db import engine

async def test_connection():
    try:
        async with engine.connect() as conn:
            print("✅ Success! Python connected to the Docker Database.")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())