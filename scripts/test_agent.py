import asyncio
from app.agent import ClinicalAgent

agent = ClinicalAgent()

async def run_test():
    result = await agent.handle_query(
        user_id=2,
        question="Where can i find info about COPD?"
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(run_test())
