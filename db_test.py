import asyncio
from db import AsyncSessionLocal
from models import User
from sqlalchemy.future import select

async def test_db():
    async with AsyncSessionLocal() as session:
        # Create a test user
        user = User(telegram_id="test_telegram_id")
        session.add(user)
        await session.commit()
        print("✅ User created!")

        # Query the user
        result = await session.execute(select(User).where(User.telegram_id == "test_telegram_id"))
        user_obj = result.scalars().first()
        if user_obj:
            print(f"✅ User found: {user_obj.telegram_id}")
        else:
            print("❌ User not found!")

        # Clean up
        await session.delete(user_obj)
        await session.commit()
        print("✅ User deleted!")

if __name__ == "__main__":
    asyncio.run(test_db()) 