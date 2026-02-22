import argparse
import json
from soul_file_engine import SoulFileEngine
from enhanced_lead_sourcing import ProductionLeadSourcingAgent

def main():
    parser = argparse.ArgumentParser(description="Digital Veteran - Production System")
    parser.add_argument('--start-dashboard', action='store_true', help='Start web dashboard')
    parser.add_argument('--generate-leads', type=int, help='Generate N production leads')
    parser.add_argument('--deploy', action='store_true', help='Deploy to production')
    parser.add_argument('--status', action='store_true', help='Check system status')
    
    args = parser.parse_args()
    
    soul_engine = SoulFileEngine()
    sourcing_agent = ProductionLeadSourcingAgent(soul_engine)
    
    if args.start_dashboard:
        import dashboard
        dashboard.app.run(host='0.0.0.0', port=5000, debug=False)
        
    elif args.generate_leads:
        count = args.generate_leads or 10
        leads = sourcing_agent.generate_production_leads(count)
        
        print(f"?? Generated {len(leads)} production leads:")
        for lead in leads[:5]:  # Show first 5
            print(f"   {lead['name']} - {lead['industry']} - Confidence: {lead['confidence_score']:.1%}")
        
        # Save to file
        with open('data/production_leads.json', 'w') as f:
            json.dump(leads, f, indent=2)
        print("?? Leads saved to data/production_leads.json")
        
    elif args.deploy:
        import deploy_production
        deploy_production.deploy_production()
        
    elif args.status:
        stats = soul_engine.get_soul_stats()
        icp_recs = soul_engine.get_current_icp_recommendations()
        
        print("?? Digital Veteran Production Status")
        print("="*40)
        print(f"?? Learning from: {stats['total_feedback_entries']} examples")
        print(f"?? Evolution cycles: {stats['evolution_cycles']}")
        print(f"?? Confidence: {icp_recs['confidence_level']:.1%}")
        print(f"?? Patterns learned: {stats['patterns_learned']}")
        
    else:
        print("Usage: python production_cli.py [--start-dashboard|--generate-leads N|--deploy|--status]")

if __name__ == "__main__":
    main()
