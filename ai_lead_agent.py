from ai_integration import AIIntegration
from lead_sourcing_agent import LeadSourcingAgent

class AIPoweredLeadSourcingAgent:
    def __init__(self, soul_engine):
        self.soul_engine = soul_engine
        self.ai = AIIntegration()
        self.base_agent = LeadSourcingAgent(soul_engine)  # Fixed variable name
    
    def generate_intelligent_leads(self, count=10):
        """Generate leads enhanced with AI analysis"""
        print("?? Generating AI-powered leads...")
        
        # Get base leads from existing agent
        base_leads = self.base_agent.generate_leads_based_on_icp(count)  # Fixed: base_agent (not base_lead_agent)
        
        # Enhance with AI analysis
        enhanced_leads = []
        for lead in base_leads:
            ai_analysis = self.ai.analyze_lead_with_ai(lead)
            lead['ai_analysis'] = ai_analysis
            lead['final_score'] = (lead.get('confidence_score', 0.5) + ai_analysis.get('score', 5)/10) / 2
            
            enhanced_leads.append(lead)
        
        print(f"? Generated {len(enhanced_leads)} AI-enhanced leads")
        return enhanced_leads
