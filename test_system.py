import os
import sys

sys.path.append(os.path.dirname(__file__))

from src.soul_file_engine import SoulFileEngine


def test_system():
    print("?? Testing Digital Veteran System...")

    # Initialize
    soul_engine = SoulFileEngine()

    # Add test feedback
    test_feedbacks = [
        {
            "lead_data": {
                "company_size": "10-50",
                "industry": "SaaS",
                "response_time_hours": 4,
                "tech_stack": ["python", "react"],
            },
            "outcome": "won",
            "revenue": 75000,
            "intangible_signals": ["fast_responder", "clear_pain_points"],
        },
        {
            "lead_data": {
                "company_size": "1000+",
                "industry": "Manufacturing",
                "response_time_hours": 72,
                "tech_stack": ["java", "oracle"],
            },
            "outcome": "lost",
            "revenue": 0,
            "intangible_signals": ["slow_responder"],
        },
        {
            "lead_data": {
                "company_size": "50-100",
                "industry": "FinTech",
                "response_time_hours": 2,
                "tech_stack": ["python", "aws", "react"],
            },
            "outcome": "whale",
            "revenue": 150000,
            "intangible_signals": ["fast_responder", "decision_maker", "high_budget"],
        },
    ]

    print("\n?? Adding test feedback...")
    for i, feedback in enumerate(test_feedbacks):
        result = soul_engine.add_feedback(feedback)
        print(
            f"   {i+1}. {feedback['outcome'].upper()} - ${feedback['revenue']} - {feedback['lead_data']['company_size']}"
        )

    # Run reflection
    print("\n?? Running reflection cycle...")
    analysis = soul_engine.run_reflection_cycle(30)
    if analysis:
        print(f"   Win rate: {analysis['win_rate']:.1%}")

    # Get recommendations
    print("\n?? ICP Recommendations:")
    recs = soul_engine.get_current_icp_recommendations()
    for key, value in recs.items():
        print(f"   {key}: {value}")

    # Show stats
    print("\n?? System Stats:")
    stats = soul_engine.get_soul_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    print("\n? Digital Veteran System Test Complete!")


if __name__ == "__main__":
    test_system()
