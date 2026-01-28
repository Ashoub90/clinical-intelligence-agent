import os
import json
from dotenv import load_dotenv
from sqlalchemy import select
from sentence_transformers import SentenceTransformer
from openai import OpenAI

from app.db import AsyncSessionLocal
from app.models import MedicalDocument, CoverageRule, User, QueryLog

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

CONFIDENCE_THRESHOLD = 0.7


# -----------------------------
# LLM-based clarification check
# -----------------------------
async def llm_needs_clarification(question: str) -> bool:
    prompt = f"""
    You are a classifier.

    Decide if the following user question is clear and specific enough
    to answer using medical guidelines (NICE) and insurance coverage rules.

    If the question is vague, ambiguous, or missing important details,
    answer ONLY with: UNCLEAR

    If the question is clear and answerable (including informational or guideline questions),
    answer ONLY with: CLEAR

    Question: "{question}"
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    decision = response.choices[0].message.content.strip().upper()
    return decision == "UNCLEAR"


class ClinicalAgent:

    async def handle_query(self, user_id: int, question: str):

        async with AsyncSessionLocal() as session:

            # 1️⃣ Clarification check (LLM-based)
            if await llm_needs_clarification(question):
                log = QueryLog(
                    user_id=user_id,
                    query=question,
                    answer="Clarification required",
                    confidence=None,
                    action="clarify",
                    retrieved_chunks=""
                )
                session.add(log)
                await session.commit()

                return {
                    "message": "Could you please clarify which medication, treatment, or condition you are asking about?"
                }

            # 2️⃣ Fetch user
            user = (await session.execute(
                select(User).where(User.id == user_id)
            )).scalar_one_or_none()

            if not user:
                return {"status": "error", "message": "User not found"}

            # 3️⃣ Embed query
            query_embedding = model.encode(question).tolist()

            # 4️⃣ Vector search (RAG)
            result = await session.execute(
                select(MedicalDocument.filename, MedicalDocument.content)
                .order_by(MedicalDocument.embedding.cosine_distance(query_embedding))
                .limit(5)
            )
            chunks = result.all()

            if not chunks:
                log = QueryLog(
                    user_id=user_id,
                    query=question,
                    answer="No relevant medical context found",
                    confidence=0.0,
                    action="escalate",
                    retrieved_chunks=""
                )
                session.add(log)
                await session.commit()

                return {
                    "status": "escalate",
                    "message": "I could not find relevant medical guidelines. This will be reviewed by a human agent."
                }

            context = "\n\n".join([c.content[:400] for c in chunks])
            retrieved_chunk_names = ", ".join([c.filename for c in chunks])

            # 5️⃣ Coverage rules
            rules = (await session.execute(
                select(CoverageRule).where(CoverageRule.plan == user.plan)
            )).scalars().all()

            rules_text = "\n".join([
                f"- {r.treatment_type}: covered={r.covered}, notes={r.notes}"
                for r in rules
            ])

            # 6️⃣ Prompt (general-purpose + JSON)
            prompt = f"""
            You are a clinical insurance assistant.

            Answer the user's question using ONLY:
            1. The provided medical guidelines context (NICE)
            2. The provided insurance coverage rules

            User plan: {user.plan}

            Insurance coverage rules:
            {rules_text}

            Medical guidelines context:
            {context}

            User question:
            {question}

            Instructions:
            - Provide a clear, helpful, user-friendly answer.
            - If the question is about coverage, explain whether it is covered and under what conditions.
            - If the question is open-ended, summarize the relevant medical guidance.
            - Do NOT invent information outside the provided context.
            - If the information is insufficient, say so.

            Return ONLY valid JSON in this format:

            {{
            "answer": "<natural language answer for the user>",
            "confidence": <number between 0 and 1>
            }}
            """

            # 7️⃣ OpenAI call
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            raw_output = response.choices[0].message.content.strip()

            # 8️⃣ Parse JSON safely
            try:
                data = json.loads(raw_output)
                answer_text = data["answer"]
                confidence = float(data["confidence"])
            except Exception:
                answer_text = "I could not generate a reliable answer. This will be reviewed by a human agent."
                confidence = 0.0

            # 9️⃣ HITL decision
            if confidence < CONFIDENCE_THRESHOLD:
                action = "escalate"
            else:
                action = "answer"

            # 🔟 Log to database (internal)
            log = QueryLog(
                user_id=user_id,
                query=question,
                answer=answer_text,
                confidence=confidence,
                action=action,
                retrieved_chunks=retrieved_chunk_names
            )
            session.add(log)
            await session.commit()

            # 1️⃣1️⃣ Return user-facing response (hide confidence)
            if action == "answer":
                return {
                    "answer": answer_text
                }

            elif action == "escalate":
                return {
                    "message": "Your request requires review by a human specialist. Please wait for confirmation."
                }
