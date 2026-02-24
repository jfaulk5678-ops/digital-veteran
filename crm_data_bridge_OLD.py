import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime, timedelta

from src.soul_file_engine import SoulFileEngine


class CRMDataBridge:
    def __init__(self, soul_engine: SoulFileEngine):
        self.soul_engine = soul_engine

    def simulate_crm_data(self):
        """Create realistic sample CRM data"""
        sample_data = [
            {
                "company": "TechStart Inc",
                "company_size": "10-50",
                "industry": "SaaS",
                "outcome": "won",
                "revenue": 75000,
                "response_time_hours": 2,
                "deal_size": "medium",
                "close_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            },
            {
                "company": "BigCorp Ltd",
                "company_size": "1000+",
                "industry": "Manufacturing",
                "outcome": "lost",
                "revenue": 0,
                "response_time_hours": 72,
                "deal_size": "large",
                "close_date": (datetime.now() - timedelta(days=10)).strftime(
                    "%Y-%m-%d"
                ),
            },
        ]
        return sample_data

    def import_recent_outcomes(self, days_back: int = 30):
        """Import recent outcomes"""
        print(f"?? Importing outcomes from last {days_back} days...")
        outcomes = self.simulate_crm_data()
        print(f"?? Found {len(outcomes)} outcomes")
        return outcomes

    def process_outcomes_to_soul(self, outcomes):
        """Process outcomes into soul file"""
        processed_count = 0
        for outcome in outcomes:
            soul_feedback = self._transform_crm_to_soul(outcome)
            self.soul_engine.add_feedback(soul_feedback)
            processed_count += 1
        print(f"? Processed {processed_count} outcomes")
        return processed_count

    def _transform_crm_to_soul(self, crm_outcome):
        """Transform CRM data to soul format"""
        return {
            "lead_data": {
                "company_size": crm_outcome.get("company_size", ""),
                "industry": crm_outcome.get("industry", ""),
                "response_time_hours": crm_outcome.get("response_time_hours", 48),
                "company_name": crm_outcome.get("company", ""),
            },
            "outcome": crm_outcome.get("outcome", "unknown"),
            "revenue": crm_outcome.get("revenue", 0),
            "intangible_signals": [],
        }


if __name__ == "__main__":
    print("Testing CRM Data Bridge...")
    soul_engine = SoulFileEngine()
    bridge = CRMDataBridge(soul_engine)

    outcomes = bridge.import_recent_outcomes(30)
    bridge.process_outcomes_to_soul(outcomes)

    recs = soul_engine.get_current_icp_recommendations()
    print("Final ICP:", recs)
