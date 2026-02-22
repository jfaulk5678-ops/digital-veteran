from flask import Flask, render_template, jsonify, request
from soul_file_engine import SoulFileEngine
from lead_sourcing_agent import LeadSourcingAgent
import json
import os

def create_app():
    app = Flask(__name__)
    
    # Production configuration
    app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Global instances
    soul_engine = SoulFileEngine()
    sourcing_agent = LeadSourcingAgent(soul_engine)

    @app.route('/')
    def dashboard():
        """Main dashboard page"""
        stats = soul_engine.get_soul_stats()
        icp_recs = soul_engine.get_current_icp_recommendations()
        
        return render_template('dashboard.html', 
                            stats=stats, 
                            icp_recs=icp_recs,
                            feedback_count=stats['total_feedback_entries'])

    @app.route('/api/stats')
    def api_stats():
        """API endpoint for system statistics"""
        return jsonify(soul_engine.get_soul_stats())

    @app.route('/api/icp')
    def api_icp():
        """API endpoint for ICP recommendations"""
        return jsonify(soul_engine.get_current_icp_recommendations())

    @app.route('/api/leads')
    def api_leads():
        """API endpoint for generated leads"""
        count = request.args.get('count', 5, type=int)
        leads = sourcing_agent.generate_leads_based_on_icp(count)
        scored_leads = sourcing_agent.score_leads(leads)
        return jsonify(scored_leads)

    @app.route('/api/feedback', methods=['POST'])
    def api_add_feedback():
        """API endpoint to add feedback"""
        try:
            feedback_data = request.get_json()
            result = soul_engine.add_feedback(feedback_data)
            return jsonify({"status": "success", "result": result})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    @app.route('/api/reflect', methods=['POST'])
    def api_reflect():
        """API endpoint to run reflection cycle"""
        try:
            analysis = soul_engine.run_reflection_cycle(7)
            return jsonify({"status": "success", "analysis": analysis})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    return app

# Create app instance
app = create_app()

if __name__ == "__main__":
    # Development mode only
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
