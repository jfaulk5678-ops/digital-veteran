import argparse
import json
from soul_file_engine import SoulFileEngine
from crm_data_bridge import CRMDataBridge
from lead_sourcing_agent import LeadSourcingAgent

def main():
    parser = argparse.ArgumentParser(description="Digital Veteran - Complete System")
    parser.add_argument('--test', action='store_true', help='Run system test')
    parser.add_argument('--generate-leads', type=int, help='Generate N leads based on ICP')
    parser.add_argument('--add-feedback', type=str, help='Add manual feedback (use single quotes)')
    parser.add_argument('--reflect', action='store_true', help='Run reflection cycle')
    parser.add_argument('--import-crm', action='store_true', help='Import from CRM and learn')
    parser.add_argument('--show-icp', action='store_true', help='Show ICP recommendations')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--demo', action='store_true', help='Run full demonstration')
    
    args = parser.parse_args()
    
    try:
        soul_engine = SoulFileEngine()
        data_bridge = CRMDataBridge(soul_engine)
        sourcing_agent = LeadSourcingAgent(soul_engine)
        
        if args.demo:
            run_demo(soul_engine, data_bridge, sourcing_agent)
            
        elif args.test:
            run_test(soul_engine, data_bridge, sourcing_agent)
            
        elif args.generate_leads:
            count = args.generate_leads or 5
            leads = sourcing_agent.generate_leads_based_on_icp(count)
            scored_leads = sourcing_agent.score_leads(leads)
            
            print(f"\n?? Generated {len(scored_leads)} leads:")
            for lead in scored_leads:
                print(f"   {lead['company_name']} - Confidence: {lead['confidence_score']:.1%}")
                
        elif args.add_feedback:
            try:
                # Handle PowerShell JSON formatting issues
                json_str = args.add_feedback.replace("'", '"')
                feedback_data = json.loads(json_str)
                soul_engine.add_feedback(feedback_data)
                print("? Feedback added successfully")
            except Exception as e:
                print(f"? Error parsing feedback: {e}")
                
        elif args.reflect:
            analysis = soul_engine.run_reflection_cycle(7)
            if analysis:
                print(f"?? Reflection complete. Win rate: {analysis['win_rate']:.1%}")
                
        elif args.import_crm:
            outcomes = data_bridge.import_recent_outcomes(30)
            processed = data_bridge.process_outcomes_to_soul(outcomes)
            print(f"? CRM data imported: {processed} outcomes")
                
        elif args.show_icp:
            recs = soul_engine.get_current_icp_recommendations()
            print("?? Current ICP Recommendations:")
            print(json.dumps(recs, indent=2))
            
        elif args.stats:
            stats = soul_engine.get_soul_stats()
            print("?? System Statistics:")
            print(json.dumps(stats, indent=2))
            
        else:
            show_help()
            
    except Exception as e:
        print(f"? Error: {e}")

def run_demo(soul_engine, data_bridge, sourcing_agent):
    """Run a complete demonstration"""
    print("?? DIGITAL VETERAN DEMONSTRATION")
    print("="*50)
    
    # 1. Show initial state
    print("\n1. Initial State:")
    stats = soul_engine.get_soul_stats()
    print(f"   Learning from: {stats['total_feedback_entries']} examples")
    
    # 2. Generate leads based on empty knowledge
    print("\n2. Generating initial leads...")
    leads = sourcing_agent.generate_leads_based_on_icp(3)
    for lead in leads:
        print(f"   {lead['company_name']} - Confidence: {lead['confidence_score']:.1%}")
    
    # 3. Add some feedback
    print("\n3. Adding feedback to learn from...")
    feedback_examples = [
        {
            "lead_data": {"company_size": "10-50", "industry": "SaaS"},
            "outcome": "won",
            "revenue": 80000
        }
    ]
    
    for feedback in feedback_examples:
        soul_engine.add_feedback(feedback)
    
    # 4. Run reflection
    print("\n4. Learning from feedback...")
    soul_engine.run_reflection_cycle(7)
    
    # 5. Generate improved leads
    print("\n5. Generating improved leads...")
    improved_leads = sourcing_agent.generate_leads_based_on_icp(3)
    for lead in improved_leads:
        print(f"   {lead['company_name']} - Confidence: {lead['confidence_score']:.1%}")
    
    print("\n? Demonstration complete! The system is learning.")

def run_test(soul_engine, data_bridge, sourcing_agent):
    """Run system test"""
    print("?? SYSTEM TEST")
    
    # Test feedback addition
    test_feedback = {
        "lead_data": {"company_size": "50-100", "industry": "FinTech"},
        "outcome": "won", 
        "revenue": 150000
    }
    soul_engine.add_feedback(test_feedback)
    print("? Feedback test passed")
    
    # Test lead generation
    leads = sourcing_agent.generate_leads_based_on_icp(2)
    print("? Lead generation test passed")
    
    # Test reflection
    analysis = soul_engine.run_reflection_cycle(1)
    print("? Reflection test passed")
    
    print("\n?? All tests passed!")

def show_help():
    print("?? DIGITAL VETERAN - AI Lead Generation System")
    print("="*50)
    print("Commands:")
    print("  --demo           # Run full demonstration")
    print("  --test           # Run system test")
    print("  --generate-leads 5  # Generate 5 leads")
    print("  --add-feedback   # Add feedback (use careful JSON)")
    print("  --reflect        # Run learning cycle")
    print("  --import-crm     # Import CRM data")
    print("  --show-icp       # Show recommendations") 
    print("  --stats          # Show system stats")
    print("\nExample: python cli.py --generate-leads 10")

if __name__ == "__main__":
    main()
