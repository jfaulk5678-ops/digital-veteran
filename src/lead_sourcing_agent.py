import os
import sys

sys.path.append(os.path.dirname(__file__))

import json
from datetime import datetime

import requests

from src.soul_file_engine import SoulFileEngine


class LeadSourcingAgent:
    def __init__(self, soul_engine: SoulFileEngine):
        self.soul_engine = soul_engine
        self.lead_sources = []

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

        # Use the learned patterns to create realistic leads
        target_signals = icp_recs.get("target_signals", [])
        avoid_signals = icp_recs.get("avoid_signals", [])

        print(f"   Targeting: {target_signals}")
        print(f"   Avoiding: {avoid_signals}")

        # Mock lead generation based on learned patterns
        for i in range(count):
            lead = self._create_mock_lead(i, target_signals, avoid_signals)
            leads.append(lead)

        return leads

    def _create_mock_lead(
        self, lead_id: int, target_signals: list, avoid_signals: list
    ):
        """Create a mock lead that matches learned patterns"""

        # Prioritize leads that match target signals
        if "company_size_10-50_positive" in target_signals:
            company_size = "10-50"
            industry = "SaaS"  # Learned positive pattern
        elif "company_size_50-100_positive" in target_signals:
            company_size = "50-100"
            industry = "FinTech"  # Whale pattern
        else:
            company_size = "100-500"
            industry = "Tech"

        # Avoid negative patterns
        if "industry_Manufacturing_caution" in avoid_signals:
            industry = "SaaS"  # Avoid manufacturing

        lead = {
            "lead_id": f"lead_{lead_id}_{datetime.now().strftime('%Y%m%d')}",
            "company_name": f"TestCompany{lead_id}",
            "company_size": company_size,
            "industry": industry,
            "revenue_potential": 50000 if company_size == "10-50" else 120000,
            "confidence_score": self._calculate_lead_confidence(
                company_size, industry, target_signals
            ),
            "generated_at": datetime.now().isoformat(),
            "source": "mock_generator",
        }

        return lead

    def _calculate_lead_confidence(
        self, company_size: str, industry: str, target_signals: list
    ) -> float:
        """Calculate how well this lead matches learned patterns"""
        confidence = 0.5  # Base confidence

        # Boost confidence for matching positive signals
        if f"company_size_{company_size}_positive" in target_signals:
            confidence += 0.3

        if (
            industry.lower() in ["saas", "fintech"]
            and "high_ticket_positive" in target_signals
        ):
            confidence += 0.2

        return min(1.0, confidence)

    def score_and_filter_leads(self, leads: list, min_confidence: float = 0.6):
        """Score leads and filter by confidence threshold"""
        scored_leads = []

        for lead in leads:
            lead["icp_match_score"] = lead.get("confidence_score", 0.5)
            lead["recommendation"] = (
                "Pursue" if lead["icp_match_score"] >= min_confidence else "Review"
            )

            scored_leads.append(lead)

        # Sort by confidence score
        scored_leads.sort(key=lambda x: x["icp_match_score"], reverse=True)

        high_confidence = [l for l in scored_leads if l["recommendation"] == "Pursue"]
        print(f"?? High-confidence leads: {len(high_confidence)}/{len(scored_leads)}")

        return scored_leads


# Test the Lead Sourcing Agent
if __name__ == "__main__":
    print("Testing Lead Sourcing Agent...")

    soul_engine = SoulFileEngine()
    sourcing_agent = LeadSourcingAgent(soul_engine)

    # Generate leads based on current ICP
    leads = sourcing_agent.generate_leads_based_on_icp(5)

    # Score and filter leads
    scored_leads = sourcing_agent.score_and_filter_leads(leads)

    print("\n?? Generated Leads:")
    for lead in scored_leads:
        print(
            f"   {lead['company_name']} - Score: {lead['icp_match_score']:.1%} - {lead['recommendation']}"
        )
