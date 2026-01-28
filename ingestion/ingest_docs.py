import os
import fitz
import asyncio
from sentence_transformers import SentenceTransformer
from app.db import AsyncSessionLocal
from app.models import MedicalDocument

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def get_chunks(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


async def ingest_pdfs():
    # Safer path handling
    base_dir = os.path.dirname(__file__)
    data_folder = os.path.join(base_dir, "..", "data", "raw_docs")

    async with AsyncSessionLocal() as session:
        for filename in os.listdir(data_folder):
            if not filename.lower().endswith(".pdf"):
                continue

            print(f"📄 Processing {filename}...")
            path = os.path.join(data_folder, filename)

            doc = fitz.open(path)
            full_text = ""

            for page in doc:
                full_text += page.get_text()

            chunks = get_chunks(full_text)
            print(f"✂️ Split into {len(chunks)} chunks.")

            for i, chunk_text in enumerate(chunks):
                embedding = model.encode(chunk_text).tolist()

                new_doc = MedicalDocument(
                    filename=f"{filename}_chunk_{i}",
                    content=chunk_text,
                    embedding=embedding
                )
                session.add(new_doc)

        await session.commit()
        print("✅ All PDFs ingested successfully.")


if __name__ == "__main__":
    asyncio.run(ingest_pdfs())
