from datetime import datetime

from soul_file_engine import SoulFileEngine


class LeadSourcingAgent:
    def __init__(self, soul_engine: SoulFileEngine):
        self.soul_engine = soul_engine

    def generate_leads_based_on_icp(self, count: int = 10):
        """Generate leads based on current ICP recommendations"""
        print("?? Generating leads based on learned ICP...")

        # Get current recommendations
        icp_recs = self.soul_engine.get_current_icp_recommendations()

        # Generate mock leads based on learned patterns
        leads = self._generate_mock_leads(count, icp_recs)

        print(f"? Generated {len(leads)} leads based on ICP patterns")
        return leads

    def _generate_mock_leads(self, count: int, icp_recs: dict):
        """Generate mock leads simulating real lead generation"""
        leads = []

        target_signals = icp_recs.get("target_signals", [])
        avoid_signals = icp_recs.get("avoid_signals", [])

        print(f"   Targeting signals: {target_signals}")
        print(f"   Avoiding signals: {avoid_signals}")

        for i in range(count):
            lead = self._create_mock_lead(i, target_signals, avoid_signals)
            leads.append(lead)

        return leads

    def _create_mock_lead(
        self, lead_id: int, target_signals: list, avoid_signals: list
    ):
        """Create a mock lead that matches learned patterns"""

        # Use learned patterns to create realistic leads
        if any("10-50" in signal for signal in target_signals):
            company_size = "10-50"
            industry = "SaaS"
            revenue_potential = 75000
        elif any("50-100" in signal for signal in target_signals):
            company_size = "50-100"
            industry = "FinTech"
            revenue_potential = 120000
        else:
            company_size = "100-500"
            industry = "Tech"
            revenue_potential = 50000

        # Avoid negative patterns
        if "Manufacturing" in str(avoid_signals):
            industry = "SaaS"  # Switch to positive industry

        lead = {
            "lead_id": f"lead_{lead_id}",
            "company_name": f"Acme{industry}{lead_id}",
            "company_size": company_size,
            "industry": industry,
            "revenue_potential": revenue_potential,
            "confidence_score": self._calculate_lead_confidence(
                company_size, industry, target_signals
            ),
            "generated_at": datetime.now().isoformat(),
        }

        return lead

    def _calculate_lead_confidence(
        self, company_size: str, industry: str, target_signals: list
    ) -> float:
        """Calculate confidence based on ICP match"""
        confidence = 0.5

        # Match company size patterns
        if any(company_size in signal for signal in target_signals):
            confidence += 0.3

        # Match industry patterns
        if industry.lower() in ["saas", "fintech"]:
            confidence += 0.2

        return min(1.0, confidence)

    def score_leads(self, leads: list):
        """Score and sort leads by confidence"""
        for lead in leads:
            lead["recommendation"] = (
                "HIGH"
                if lead["confidence_score"] > 0.7
                else "MEDIUM" if lead["confidence_score"] > 0.5 else "LOW"
            )

        leads.sort(key=lambda x: x["confidence_score"], reverse=True)
        return leads


# Test function
def test_lead_generation():
    print("Testing Lead Generation...")
    soul_engine = SoulFileEngine()
    agent = LeadSourcingAgent(soul_engine)

    # Generate leads
    leads = agent.generate_leads_based_on_icp(5)
    scored_leads = agent.score_leads(leads)

    print("\n?? Generated Leads:")
    for lead in scored_leads:
        print(
            f"   {lead['company_name']} - Size: {lead['company_size']} - Confidence: {lead['confidence_score']:.1%} - {lead['recommendation']}"
        )


if __name__ == "__main__":
    test_lead_generation()
