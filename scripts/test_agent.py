import asyncio
from app.agent import ClinicalAgent

agent = ClinicalAgent()

async def run_test():
    result = await agent.handle_query(
        user_id=1,
        question="Is insulin covered for type 2 diabetes?"
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(run_test())
