import asyncio
from app.db import AsyncSessionLocal
from app.models import User


async def seed_users():
    async with AsyncSessionLocal() as session:

        users = [
            User(name="Alice Hassan", plan="Silver", age=45),
            User(name="Mohamed Ali", plan="Gold", age=60),
            User(name="Sara Ahmed", plan="Bronze", age=30),
        ]

        session.add_all(users)
        await session.commit()
        print("✅ Users seeded successfully.")

        await session.close()


if __name__ == "__main__":
    asyncio.run(seed_users())
