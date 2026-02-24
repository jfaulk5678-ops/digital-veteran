import os

from flask import Flask, jsonify, render_template, request

from lead_sourcing_agent import LeadSourcingAgent
from soul_file_engine import SoulFileEngine


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["ENV"] = os.getenv("FLASK_ENV", "production")

    # Create templates directory
    os.makedirs("templates", exist_ok=True)

    # Global instances
    soul_engine = SoulFileEngine()
    sourcing_agent = LeadSourcingAgent(soul_engine)

    @app.route("/")
    def dashboard():
        """Main dashboard page"""
        stats = soul_engine.get_soul_stats()
        icp_recs = soul_engine.get_current_icp_recommendations()

        return render_template("dashboard.html", stats=stats, icp_recs=icp_recs)

    @app.route("/api/stats")
    def api_stats():
        return jsonify(soul_engine.get_soul_stats())

    @app.route("/api/icp")
    def api_icp():
        return jsonify(soul_engine.get_current_icp_recommendations())

    @app.route("/api/leads")
    def api_leads():
        count = request.args.get("count", 5, type=int)
        leads = sourcing_agent.generate_leads_based_on_icp(count)
        scored_leads = sourcing_agent.score_leads(leads)
        return jsonify(scored_leads)

    # NEW AI ROUTES
    @app.route("/api/ai-analyze", methods=["POST"])
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

    @app.route("/api/ai-leads")
    def api_ai_leads():
        """Get AI-enhanced leads"""
        try:
            from ai_lead_agent import AIPoweredLeadSourcingAgent

            ai_agent = AIPoweredLeadSourcingAgent(soul_engine)

            count = request.args.get("count", 5, type=int)
            leads = ai_agent.generate_intelligent_leads(count)

            return jsonify(leads)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    # Create simple template
    with open("templates/dashboard.html", "w") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Digital Veteran</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .card { background: #f5f5f5; padding: 20px; margin: 10px 0; border-radius: 8px; }
        .ai-section { background: #e3f2fd; padding: 15px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>?? Digital Veteran - AI Powered</h1>
    
    <div class="card">
        <h3>System Stats</h3>
        <p>Feedback Entries: {{ stats.total_feedback_entries }}</p>
        <p>Evolution Cycles: {{ stats.evolution_cycles }}</p>
    </div>
    
    <div class="card">
        <h3>ICP Recommendations</h3>
        <p>Confidence: {{ (icp_recs.confidence_level * 100)|round(1) }}%</p>
    </div>

    <div class="ai-section">
        <h3>?? AI Features</h3>
        <p><a href="/api/ai-leads?count=3">Get AI-Enhanced Leads</a></p>
        <p>Ollama Integration: Active</p>
    </div>
</body>
</html>
        """)

    return app


# Create app instance
app = create_app()

if __name__ == "__main__":
    # Development mode only
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
