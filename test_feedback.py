# test_feedback.py
import json

from soul_file_engine import SoulFileEngine


def test_add_feedback():
    soul_engine = SoulFileEngine()

    # Test feedback data
    feedback_examples = [
        {
            "lead_data": {
                "company_size": "10-50",
                "industry": "Tech",
                "response_time_hours": 4,
            },
            "outcome": "won",
            "revenue": 50000,
            "intangible_signals": ["fast_responder", "clear_pain_points"],
        },
        {
            "lead_data": {
                "company_size": "1000+",
                "industry": "Manufacturing",
                "response_time_hours": 72,
            },
            "outcome": "lost",
            "revenue": 0,
            "intangible_signals": ["slow_responder"],
        },
    ]

    for i, feedback in enumerate(feedback_examples):
        result = soul_engine.add_feedback(feedback)
        print(f"? Added feedback {i+1}: {result['outcome']} outcome")

    # Run reflection
    analysis = soul_engine.run_reflection_cycle(7)
    if analysis:
        print(f"?? Reflection complete. Win rate: {analysis['win_rate']:.1%}")

    # Show results
    recs = soul_engine.get_current_icp_recommendations()
    print("\n?? Current ICP Recommendations:")
    print(json.dumps(recs, indent=2))


if __name__ == "__main__":
    test_add_feedback()
