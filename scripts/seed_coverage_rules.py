import asyncio
from app.db import AsyncSessionLocal
from app.models import CoverageRule


async def seed_coverage_rules():
    async with AsyncSessionLocal() as session:

        rules = [
            CoverageRule(plan="Silver", treatment_type="medication", covered=True,
                         notes="Covered with standard formulary"),

            CoverageRule(plan="Silver", treatment_type="injection", covered=True,
                         notes="Requires prior authorization"),

            CoverageRule(plan="Silver", treatment_type="surgery", covered=False,
                         notes="Only covered in emergency cases"),

            CoverageRule(plan="Gold", treatment_type="medication", covered=True,
                         notes="Fully covered"),

            CoverageRule(plan="Gold", treatment_type="injection", covered=True,
                         notes="Fully covered"),

            CoverageRule(plan="Gold", treatment_type="surgery", covered=True,
                         notes="Covered"),

            CoverageRule(plan="Bronze", treatment_type="medication", covered=True,
                         notes="Generic medications only"),

            CoverageRule(plan="Bronze", treatment_type="injection", covered=False,
                         notes="Not covered")
        ]

        session.add_all(rules)
        await session.commit()
        print("✅ Coverage rules seeded successfully.")

        await session.close()


if __name__ == "__main__":
    asyncio.run(seed_coverage_rules())
