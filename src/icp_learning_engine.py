import json
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd


class ICPLearningEngine:
    def __init__(self):
        self.knowledge_base = {
            "positive_signals": [],
            "negative_signals": [],
            "competitor_gaps": [],
            "conversion_patterns": [],
            "feedback_loops": [],
        }

    def add_feedback(self, lead_data: Dict, outcome: str):
        """Add feedback to train the ICP model"""
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "lead_data": lead_data,
            "outcome": outcome,  # "hit", "miss", "converted", "lost"
            "lessons_learned": self._extract_lessons(lead_data, outcome),
        }

        self.knowledge_base["feedback_loops"].append(feedback)

        if outcome in ["hit", "converted"]:
            self.knowledge_base["positive_signals"].extend(feedback["lessons_learned"])
        else:
            self.knowledge_base["negative_signals"].extend(feedback["lessons_learned"])

        self._refine_icp_parameters()

    def _extract_lessons(self, lead_data: Dict, outcome: str) -> List[str]:
        """Extract patterns from lead outcomes"""
        lessons = []

        # Example pattern extraction
        if outcome == "hit":
            if lead_data.get("company_size") == "10-50":
                lessons.append("ideal_company_size_10_50")
            if "saas" in lead_data.get("industry", "").lower():
                lessons.append("industry_saas_positive")

        return lessons

    def _refine_icp_parameters(self):
        """Refine ICP based on accumulated knowledge"""
        # Remove noisy signals (signals that appear in both positive and negative)
        positive_set = set(self.knowledge_base["positive_signals"])
        negative_set = set(self.knowledge_base["negative_signals"])

        # Keep only signals that strongly correlate with outcomes
        strong_signals = positive_set - negative_set
        self.knowledge_base["positive_signals"] = list(strong_signals)

    def generate_icp_profile(self) -> Dict:
        """Generate the current Ideal Customer Profile"""
        return {
            "positive_indicators": list(set(self.knowledge_base["positive_signals"])),
            "negative_indicators": list(set(self.knowledge_base["negative_signals"])),
            "confidence_score": self._calculate_confidence(),
            "last_updated": datetime.now().isoformat(),
            "total_feedback_points": len(self.knowledge_base["feedback_loops"]),
        }

    def _calculate_confidence(self) -> float:
        """Calculate how confident we are in the current ICP"""
        total_feedback = len(self.knowledge_base["feedback_loops"])
        if total_feedback == 0:
            return 0.0

        unique_signals = len(
            set(
                self.knowledge_base["positive_signals"]
                + self.knowledge_base["negative_signals"]
            )
        )

        return min(1.0, unique_signals / max(10, total_feedback))


# Example usage
if __name__ == "__main__":
    icp_engine = ICPLearningEngine()

    # Simulate some feedback
    icp_engine.add_feedback(
        {
            "company_size": "10-50",
            "industry": "SaaS",
            "funding_round": "Series A",
            "hiring_growth": "15%",
        },
        "hit",
    )

    icp_engine.add_feedback(
        {
            "company_size": "1000+",
            "industry": "Manufacturing",
            "funding_round": "None",
            "hiring_growth": "2%",
        },
        "miss",
    )

    current_icp = icp_engine.generate_icp_profile()
    print("Current ICP Profile:")
    print(json.dumps(current_icp, indent=2))
