# Add this to your dashboard.py routes

@app.route('/api/ai-analyze', methods=['POST'])
def api_ai_analyze():
    """Analyze a lead with AI"""
    try:
        from ai_integration import AIIntegration
        ai = AIIntegration()
        
        lead_data = request.get_json()
        analysis = ai.analyze_lead_with_ai(lead_data)
        
        return jsonify({"status": "success", "analysis": analysis})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/ai-leads')
def api_ai_leads():
    """Get AI-enhanced leads"""
    try:
        from ai_lead_agent import AIPoweredLeadSourcingAgent
        from soul_file_engine import SoulFileEngine
        
        soul_engine = SoulFileEngine()
        ai_agent = AIPoweredLeadSourcingAgent(soul_engine)
        
        count = request.args.get('count', 5, type=int)
        leads = ai_agent.generate_intelligent_leads(count)
        
        return jsonify(leads)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
