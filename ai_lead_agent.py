import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List

from ai_integration import AIIntegration
from lead_sourcing_agent import LeadSourcingAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIPoweredLeadSourcingAgent:
    def __init__(self, soul_engine):
        self.soul_engine = soul_engine
        self.ai = AIIntegration()
        self.base_agent = LeadSourcingAgent(soul_engine)
        self.executor = ThreadPoolExecutor(max_workers=10)  # Configurable worker count

    def _enhance_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance a single lead with AI analysis"""
        try:
            ai_analysis = self.ai.analyze_lead_with_ai(lead)
            lead["ai_analysis"] = ai_analysis
            lead["final_score"] = (
                lead.get("confidence_score", 0.5) + ai_analysis.get("score", 5) / 10
            ) / 2
            return lead
        except Exception as e:
            logger.error(f"Error enhancing lead {lead.get('id', 'unknown')}: {str(e)}")
            lead["ai_analysis"] = {"error": str(e), "score": 0}
            lead["final_score"] = (
                lead.get("confidence_score", 0.5) * 0.5
            )  # Penalize failed analyses
            return lead

    def generate_intelligent_leads(self, count=10) -> List[Dict[str, Any]]:
        """Generate leads enhanced with parallel AI analysis"""
        logger.info(f"Generating {count} AI-powered leads...")

        # Get base leads from existing agent
        base_leads = self.base_agent.generate_leads_based_on_icp(count)

        # Enhance leads with parallel processing
        enhanced_leads = []
        futures = []

        # Submit all enhancement tasks
        for lead in base_leads:
            future = self.executor.submit(self._enhance_lead, lead)
            futures.append(future)

        # Collect results as they complete
        for future in as_completed(futures):
            try:
                enhanced_lead = future.result(timeout=30)  # 30-second timeout
                enhanced_leads.append(enhanced_lead)
            except Exception as e:
                logger.error(f"Failed to process lead: {str(e)}")

        # Sort by final score (descending)
        enhanced_leads.sort(key=lambda x: x.get("final_score", 0), reverse=True)

        logger.info(f"Generated {len(enhanced_leads)} AI-enhanced leads")
        return enhanced_leads

    def shutdown(self):
        """Cleanup executor resources"""
        self.executor.shutdown(wait=True)
