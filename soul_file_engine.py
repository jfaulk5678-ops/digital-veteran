import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class SoulFileEngine:
    def __init__(self, soul_file_path: str = "config/soul_file.json"):
        self.soul_file_path = soul_file_path
        self.soul = self._load_or_create_soul()

    def _load_or_create_soul(self) -> Dict[str, Any]:
        """Load existing soul file or create initial version"""
        os.makedirs(os.path.dirname(self.soul_file_path), exist_ok=True)

        if os.path.exists(self.soul_file_path):
            try:
                with open(self.soul_file_path, "r", encoding="utf-8") as f:
                    soul_data = json.load(f)
                return self._ensure_soul_structure(soul_data)
            except (json.JSONDecodeError, IOError):
                return self._create_initial_soul()
        return self._create_initial_soul()

    def _ensure_soul_structure(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
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

        return self._deep_merge(required_structure, soul_data)

    def _deep_merge(
        self, base: Dict[str, Any], update: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deep merge two dictionaries"""
        result = base.copy()

        for key, value in update.items():
            if isinstance(result.get(key), dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def _create_initial_soul(self) -> Dict[str, Any]:
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

    def _save_soul(self, soul_data: Dict[str, Any]) -> None:
        """Save the soul file"""
        soul_data["last_updated"] = datetime.now().isoformat()
        with open(self.soul_file_path, "w", encoding="utf-8") as f:
            json.dump(soul_data, f, indent=2, ensure_ascii=False)

    def add_feedback(self, outcome_data: Dict[str, Any]) -> Dict[str, Any]:
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

    def _extract_immediate_lessons(self, feedback: Dict[str, Any]) -> None:
        """Extract immediate lessons from a single outcome"""
        outcome = feedback["outcome"]
        lead_data = feedback["lead_data"]
        current_knowledge = self.soul["current_knowledge"]

        if outcome == "won":
            if company_size := lead_data.get("company_size"):
                pattern = f"company_size_{company_size}_positive"
                if pattern not in current_knowledge["positive_patterns"]:
                    current_knowledge["positive_patterns"].append(pattern)

            if feedback.get("revenue", 0) > 50000:
                whale_signal = "high_ticket_positive"
                if whale_signal not in current_knowledge["whale_signals"]:
                    current_knowledge["whale_signals"].append(whale_signal)

        elif outcome == "lost":
            if industry := lead_data.get("industry"):
                pattern = f"industry_{industry}_caution"
                if pattern not in current_knowledge["negative_patterns"]:
                    current_knowledge["negative_patterns"].append(pattern)

    def run_reflection_cycle(self, timeframe_days: int = 7) -> Optional[Dict[str, Any]]:
        """Run a full reflection cycle"""
        recent_feedback = self._get_recent_feedback(timeframe_days)

        if not recent_feedback:
            return None

        analysis = self._analyze_patterns(recent_feedback)
        self._incorporate_analysis(analysis)
        self.soul["evolution_cycles"] += 1
        self._save_soul(self.soul)

        return analysis

    def _get_recent_feedback(self, days: int) -> List[Dict[str, Any]]:
        """Get feedback from the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)

        return [
            fb
            for fb in self.soul["feedback_history"]
            if datetime.fromisoformat(fb["timestamp"].replace("Z", "+00:00"))
            > cutoff_date
        ]

    def _analyze_patterns(self, feedback: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns across multiple outcomes"""
        wins = [f for f in feedback if f["outcome"] in ("won", "whale")]
        win_count = len(wins)
        total_count = len(feedback)

        return {
            "win_rate": win_count / total_count if total_count else 0,
            "significant_patterns": (
                [f"recent_wins_{win_count}"] if win_count > 0 else []
            ),
            "confidence_impact": (
                min(0.1, (win_count / total_count) * 0.05) if total_count else 0
            ),
        }

    def _incorporate_analysis(self, analysis: Dict[str, Any]) -> None:
        """Incorporate analysis results into soul knowledge"""
        current_conf = self.soul["current_knowledge"]["confidence_score"]
        self.soul["current_knowledge"]["confidence_score"] = min(
            0.95, current_conf + analysis["confidence_impact"]
        )

        for pattern in analysis["significant_patterns"]:
            if pattern not in self.soul["current_knowledge"]["positive_patterns"]:
                self.soul["current_knowledge"]["positive_patterns"].append(pattern)

    def get_current_icp_recommendations(self) -> Dict[str, Any]:
        """Get current ICP recommendations"""
        knowledge = self.soul["current_knowledge"]
        pos_patterns = knowledge["positive_patterns"]
        neg_patterns = knowledge["negative_patterns"]

        return {
            "target_signals": pos_patterns[-5:],
            "avoid_signals": neg_patterns[-5:],
            "whale_indicators": knowledge["whale_signals"],
            "confidence_level": knowledge["confidence_score"],
            "based_on_examples": knowledge["total_learning_examples"],
        }

    def get_soul_stats(self) -> Dict[str, Any]:
        """Get statistics about the soul file"""
        knowledge = self.soul.get("current_knowledge", {})

        return {
            "total_feedback_entries": len(self.soul.get("feedback_history", [])),
            "evolution_cycles": self.soul.get("evolution_cycles", 0),
            "patterns_learned": len(knowledge.get("positive_patterns", []))
            + len(knowledge.get("negative_patterns", [])),
            "creation_date": self.soul.get("created_date", "unknown"),
            "last_updated": self.soul.get("last_updated", "unknown"),
        }


if __name__ == "__main__":
    soul_engine = SoulFileEngine()
    stats = soul_engine.get_soul_stats()
