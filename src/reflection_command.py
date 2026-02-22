class ReflectionCommand:
    def __init__(self, soul_file_path: str):
        self.soul_file_path = soul_file_path
        
    def execute_reflection(self, outcomes_data: list):
        """The magic 'Reflect' command that makes the system 10% smarter"""
        print("?? Running Reflect Command: Analyzing outcomes for hidden patterns...")
        
        # Load current soul
        with open(self.soul_file_path, 'r') as f:
            soul = json.load(f)
            
        # Analyze patterns
        analysis = self._analyze_outcomes(outcomes_data)
        
        # Update soul file with new intelligence
        soul["current_knowledge"]["positive_patterns"] = analysis["winning_patterns"]
        soul["current_knowledge"]["negative_patterns"] = analysis["losing_patterns"] 
        soul["current_knowledge"]["confidence_score"] = analysis["confidence_gain"]
        soul["evolution_cycles"] += 1
        
        # Save updated soul
        with open(self.soul_file_path, 'w') as f:
            json.dump(soul, f, indent=2)
            
        print(f"? Soul file updated! Evolution cycle: {soul['evolution_cycles']}")
        print(f"?? Confidence increased by: {analysis['confidence_gain']:.1%}")
        
        return analysis
    
    def _analyze_outcomes(self, outcomes: list):
        """Find the non-obvious patterns that separate winners from losers"""
        winners = [o for o in outcomes if o["outcome"] in ["won", "whale"]]
        losers = [o for o in outcomes if o["outcome"] in ["lost", "churned"]]
        
        # Analyze response patterns
        winner_response_times = [w.get("response_time_hours", 48) for w in winners]
        loser_response_times = [l.get("response_time_hours", 48) for l in losers]
        
        # Analyze conversation tone patterns
        winner_tone_keywords = self._extract_tone_patterns(winners)
        loser_tone_keywords = self._extract_tone_patterns(losers)
        
        return {
            "winning_patterns": {
                "fast_response_indicators": winner_response_times,
                "positive_tone_signals": winner_tone_keywords
            },
            "losing_patterns": {
                "slow_response_indicators": loser_response_times, 
                "negative_tone_signals": loser_tone_keywords
            },
            "confidence_gain": min(0.95, len(winners) / max(1, len(outcomes)) * 0.1)
        }
