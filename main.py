import asyncio

from ai_lead_agent import AIPoweredLeadSourcingAgent
from soul_file_engine import SoulFileEngine


async def main():
    # 1. Initialize the Heart (Soul Engine)
    heart = SoulFileEngine()

    # 2. Give the Heart to the Brain (Lead Agent)
    agent = AIPoweredLeadSourcingAgent(heart)

    # 3. Run the engine
    print("Blue Ocean Engine: Analyzing Leads...")
    leads = agent.generate_intelligent_leads(count=5)

    for lead in leads:
        print(f"Found Lead: {lead}")


if __name__ == "__main__":
    asyncio.run(main())
