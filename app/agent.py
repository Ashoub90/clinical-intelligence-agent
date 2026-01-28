from sqlalchemy import select
from sentence_transformers import SentenceTransformer
from app.db import AsyncSessionLocal
from app.models import MedicalDocument, CoverageRule, User
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


class ClinicalAgent:

    async def handle_query(self, user_id: int, question: str):

        async with AsyncSessionLocal() as session:

            # 1️⃣ Fetch user
            user = (await session.execute(
                select(User).where(User.id == user_id)
            )).scalar_one_or_none()

            if not user:
                return {"status": "error", "message": "User not found"}

            # 2️⃣ Embed query
            query_embedding = model.encode(question).tolist()

            # 3️⃣ Vector search
            result = await session.execute(
                select(MedicalDocument.filename, MedicalDocument.content)
                .order_by(MedicalDocument.embedding.cosine_distance(query_embedding))
                .limit(5)
            )
            chunks = result.all()

            if not chunks:
                return {"status": "fallback", "message": "No relevant medical info found"}

            context = "\n\n".join([c.content[:400] for c in chunks])

            # 4️⃣ Coverage rules
            rules = (await session.execute(
                select(CoverageRule).where(CoverageRule.plan == user.plan)
            )).scalars().all()

            rules_text = "\n".join([
                f"- {r.treatment_type}: covered={r.covered}, notes={r.notes}"
                for r in rules
            ])

            # 5️⃣ Prompt
            prompt = f"""
            You are a clinical insurance assistant.

            User plan: {user.plan}

            Coverage rules:
            {rules_text}

            Medical guidelines context:
            {context}

            User question:
            {question}

            Answer clearly:
            1. Is the treatment covered? (yes/no/unclear)
            2. Medical justification from NICE guidelines
            3. Insurance justification from coverage rules
            4. Provide a confidence score from 0 to 1
            """

            # 6️⃣ OpenAI call
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            answer_text = response.choices[0].message.content

            return {
                "status": "success",
                "answer": answer_text,
                "sources": [c.filename for c in chunks]
            }
