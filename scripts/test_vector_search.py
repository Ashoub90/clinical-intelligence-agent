import asyncio
from sentence_transformers import SentenceTransformer
from sqlalchemy import select
from app.db import AsyncSessionLocal
from app.models import MedicalDocument

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


async def test_search():
    print("✅ Script started")

    query = "Is insulin recommended for type 2 diabetes?"
    query_embedding = model.encode(query).tolist()

    async with AsyncSessionLocal() as session:
        print("✅ DB session opened")

        stmt = (
            select(MedicalDocument.filename, MedicalDocument.content)
            .order_by(MedicalDocument.embedding.cosine_distance(query_embedding))
            .limit(3)
        )

        result = await session.execute(stmt)
        rows = result.all()

        print(f"✅ Rows fetched: {len(rows)}\n")

        for i, row in enumerate(rows, 1):
            print(f"Result {i}: {row.filename}")
            print(row.content[:400])
            print("-" * 80)


if __name__ == "__main__":
    asyncio.run(test_search())
