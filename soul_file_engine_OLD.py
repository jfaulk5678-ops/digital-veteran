import json
import os
import statistics
from datetime import datetime, timedelta


class SoulFileEngine:
    def __init__(self, soul_file_path: str = "config/soul_file.json"):
        self.soul_file_path = soul_file_path
        self.soul = self._load_or_create_soul()

    def _load_or_create_soul(self):
        """Load existing soul file or create initial version with all required keys"""
        os.makedirs(os.path.dirname(self.soul_file_path), exist_ok=True)

        if os.path.exists(self.soul_file_path):
            try:
                with open(self.soul_file_path, "r") as f:
                    soul_data = json.load(f)
                    # Ensure all required keys exist
                    return self._ensure_soul_structure(soul_data)
            except Exception as e:
                print(f"Error loading soul file: {e}, creating new one")
                return self._create_initial_soul()
        else:
            return self._create_initial_soul()

    def _ensure_soul_structure(self, soul_data):
        """Ensure the soul file has all required keys"""
        required_structure = {
            "name": "ICP Architect",
            "role": "Senior Lead Strategist & Evolution Specialist",
            "vibe": "Analytical, proactive, obsessed with high-value whale leads",
            "core_mandate": {
                "start_simple": "Begin with user's base parameters for industry and company size",
                "organize_enrich": "Find tech stack, recent news, LinkedIn activity - not just names",
                "learning_loop": "Weekly analysis of sales outcomes to find hidden patterns",
                "self_correction": "Immediately add 'Closed Lost' traits to Negative ICP",
            },
            "operating_principles": {
                "hunt_whales": "Prioritize leads mirroring highest-paying historical customers",
                "identify_intangibles": "Look beyond job titles to tone, pain points, behavioral signals",
                "proactive_evolution": "Suggest new niches when market shifts are detected",
            },
            "current_knowledge": {
                "positive_patterns": [],
                "negative_patterns": [],
                "whale_signals": [],
                "market_shifts_detected": [],
                "confidence_score": 0.0,
                "total_learning_examples": 0,
            },
            "feedback_history": [],
            "evolution_cycles": 0,
            "created_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
        }

        # Merge existing data with required structure
        return self._deep_merge(required_structure, soul_data)

    def _deep_merge(self, base, update):
        """Deep merge two dictionaries"""
        result = base.copy()

        for key, value in update.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def _create_initial_soul(self):
        """Create the initial soul file structure"""
        initial_soul = {
            "name": "ICP Architect",
            "role": "Senior Lead Strategist & Evolution Specialist",
            "vibe": "Analytical, proactive, obsessed with high-value whale leads",
            "core_mandate": {
                "start_simple": "Begin with user's base parameters for industry and company size",
                "organize_enrich": "Find tech stack, recent news, LinkedIn activity - not just names",
                "learning_loop": "Weekly analysis of sales outcomes to find hidden patterns",
                "self_correction": "Immediately add 'Closed Lost' traits to Negative ICP",
            },
            "operating_principles": {
                "hunt_whales": "Prioritize leads mirroring highest-paying historical customers",
                "identify_intangibles": "Look beyond job titles to tone, pain points, behavioral signals",
                "proactive_evolution": "Suggest new niches when market shifts are detected",
            },
            "current_knowledge": {
                "positive_patterns": [],
                "negative_patterns": [],
                "whale_signals": [],
                "market_shifts_detected": [],
                "confidence_score": 0.0,
                "total_learning_examples": 0,
            },
            "feedback_history": [],
            "evolution_cycles": 0,
            "created_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
        }

        self._save_soul(initial_soul)
        return initial_soul

    def _save_soul(self, soul_data):
        """Save the soul file"""
        soul_data["last_updated"] = datetime.now().isoformat()
        with open(self.soul_file_path, "w") as f:
            json.dump(soul_data, f, indent=2)

    def add_feedback(self, outcome_data):
        """Add a single outcome to learn from"""
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "lead_data": outcome_data.get("lead_data", {}),
            "outcome": outcome_data.get("outcome", "unknown"),
            "revenue": outcome_data.get("revenue", 0),
            "intangible_signals": outcome_data.get("intangible_signals", []),
            "lessons_extracted": [],
        }

        self.soul["feedback_history"].append(feedback_entry)
        self.soul["current_knowledge"]["total_learning_examples"] += 1
        self.soul["last_updated"] = datetime.now().isoformat()

        self._extract_immediate_lessons(feedback_entry)
        self._save_soul(self.soul)

        return feedback_entry

    def _extract_immediate_lessons(self, feedback):
        """Extract immediate lessons from a single outcome"""
        outcome = feedback["outcome"]
        lead_data = feedback["lead_data"]

        if outcome == "won":
            if lead_data.get("company_size"):
                pattern = f"company_size_{lead_data['company_size']}_positive"
                if pattern not in self.soul["current_knowledge"]["positive_patterns"]:
                    self.soul["current_knowledge"]["positive_patterns"].append(pattern)

            if feedback.get("revenue", 0) > 50000:
                whale_signal = "high_ticket_positive"
                if whale_signal not in self.soul["current_knowledge"]["whale_signals"]:
                    self.soul["current_knowledge"]["whale_signals"].append(whale_signal)

        elif outcome == "lost":
            if lead_data.get("industry"):
                pattern = f"industry_{lead_data['industry']}_caution"
                if pattern not in self.soul["current_knowledge"]["negative_patterns"]:
                    self.soul["current_knowledge"]["negative_patterns"].append(pattern)

    def run_reflection_cycle(self, timeframe_days: int = 7):
        """Run a full reflection cycle"""
        print(f"?? Running Reflection Cycle: Analyzing last {timeframe_days} days...")

        recent_feedback = self._get_recent_feedback(timeframe_days)

        if not recent_feedback:
            print("No recent feedback to analyze")
            return None

        analysis = self._analyze_patterns(recent_feedback)
        self._incorporate_analysis(analysis)
        self.soul["evolution_cycles"] += 1
        self._save_soul(self.soul)

        print(
            f"? Reflection complete! Evolution cycle: {self.soul['evolution_cycles']}"
        )
        return analysis

    def _get_recent_feedback(self, days):
        """Get feedback from the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent = []

        for fb in self.soul["feedback_history"]:
            try:
                fb_date = datetime.fromisoformat(fb["timestamp"].replace("Z", "+00:00"))
                if fb_date > cutoff_date:
                    recent.append(fb)
            except:
                continue

        return recent

    def _analyze_patterns(self, feedback):
        """Analyze patterns across multiple outcomes"""
        wins = [f for f in feedback if f["outcome"] in ["won", "whale"]]
        losses = [f for f in feedback if f["outcome"] in ["lost", "churned"]]

        analysis = {
            "win_rate": len(wins) / len(feedback) if feedback else 0,
            "significant_patterns": [],
            "confidence_impact": 0.0,
        }

        if len(wins) > 0:
            analysis["significant_patterns"].append(f"recent_wins_{len(wins)}")

        analysis["confidence_impact"] = min(0.1, analysis["win_rate"] * 0.05)

        return analysis

    def _incorporate_analysis(self, analysis):
        """Incorporate analysis results into soul knowledge"""
        current_conf = self.soul["current_knowledge"].get("confidence_score", 0)
        self.soul["current_knowledge"]["confidence_score"] = min(
            0.95, current_conf + analysis["confidence_impact"]
        )

        for pattern in analysis["significant_patterns"]:
            if pattern not in self.soul["current_knowledge"]["positive_patterns"]:
                self.soul["current_knowledge"]["positive_patterns"].append(pattern)

    def get_current_icp_recommendations(self):
        """Get current ICP recommendations"""
        return {
            "target_signals": self.soul["current_knowledge"]["positive_patterns"][-5:],
            "avoid_signals": self.soul["current_knowledge"]["negative_patterns"][-5:],
            "whale_indicators": self.soul["current_knowledge"]["whale_signals"],
            "confidence_level": self.soul["current_knowledge"].get(
                "confidence_score", 0
            ),
            "based_on_examples": self.soul["current_knowledge"].get(
                "total_learning_examples", 0
            ),
        }

    def get_soul_stats(self):
        """Get statistics about the soul file - with safe key access"""
        stats = {
            "total_feedback_entries": len(self.soul.get("feedback_history", [])),
            "evolution_cycles": self.soul.get("evolution_cycles", 0),
            "patterns_learned": len(
                self.soul.get("current_knowledge", {}).get("positive_patterns", [])
            )
            + len(self.soul.get("current_knowledge", {}).get("negative_patterns", [])),
        }

        # Safe date access
        stats["creation_date"] = self.soul.get("created_date", "unknown")
        stats["last_updated"] = self.soul.get("last_updated", "unknown")

        return stats


# Test the robust version
if __name__ == "__main__":
    try:
        print("?? Testing Robust Soul File Engine...")
        soul_engine = SoulFileEngine()

        print("?? Soul Stats:")
        stats = soul_engine.get_soul_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")

        print("? Soul file engine is working correctly!")

    except Exception as e:
        print(f"? Error: {e}")
        import traceback

        traceback.print_exc()
