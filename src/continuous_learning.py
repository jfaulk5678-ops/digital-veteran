class ContinuousLearningEngine:
    def __init__(self):
        self.feedback_history = []
        self.market_signals = []
        
    def add_sales_outcome(self, lead_data: dict, outcome: str, revenue: float = 0):
        """Add a sales outcome to learn from"""
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "lead_data": lead_data,
            "outcome": outcome,  # "won", "lost", "churned", "whale"
            "revenue": revenue,
            "intangible_signals": self._extract_intangibles(lead_data)
        }
        
        self.feedback_history.append(feedback)
        
        # Immediate pattern detection
        if outcome == "won" and revenue > 100000:  # Whale detected
            self._identify_whale_patterns(lead_data)
            
        return self._calculate_learning_impact(feedback)
    
    def _extract_intangibles(self, lead_data: dict) -> list:
        """Extract the 'gut feel' signals"""
        intangibles = []
        
        # Response enthusiasm
        if lead_data.get("response_enthusiasm") == "high":
            intangibles.append("high_engagement")
            
        # Pain point specificity
        if lead_data.get("pain_articulation") == "specific":
            intangibles.append("clear_problem_awareness")
            
        # Decision maker access
        if lead_data.get("decision_maker_accessible"):
            intangibles.append("short_sales_cycle")
            
        return intangibles
    
    def _identify_whale_patterns(self, whale_lead: dict):
        """Identify what makes a whale different"""
        print(f"?? WHALE DETECTED: Analyzing patterns for ${whale_lead.get('revenue', 0)} deal")
        
        # Add to whale signals
        whale_signals = [
            "high_revenue_potential",
            "long_term_potential", 
            "strategic_partner_fit"
        ]
        
        # Also look for behavioral whales (not just revenue)
        if whale_lead.get("strategic_fit_score") > 0.8:
            whale_signals.append("high_strategic_alignment")

class WeeklyReflectionEngine:
    def __init__(self, learning_engine: ContinuousLearningEngine):
        self.learning_engine = learning_engine
        
    def run_weekly_analysis(self):
        """Friday analysis - the core learning loop"""
        recent_feedback = self._get_recent_feedback(7)  # Last 7 days
        
        insights = {
            "win_patterns": self._analyze_wins(recent_feedback),
            "loss_patterns": self._analyze_losses(recent_feedback),
            "market_shifts": self._detect_market_shifts(recent_feedback),
            "recommended_icp_updates": self._generate_icp_updates(recent_feedback)
        }
        
        return insights
