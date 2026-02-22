from flask import Flask, render_template, jsonify, request
from soul_file_engine import SoulFileEngine
from lead_sourcing_agent import LeadSourcingAgent
import json
import os

app = Flask(__name__)

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

if __name__ == '__main__':
    # Create templates directory
    os.makedirs('templates', exist_ok=True)
    
    # Create simple dashboard template
    with open('templates/dashboard.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Digital Veteran Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background: #f5f5f5; padding: 20px; border-radius: 8px; }
        .leads { grid-column: 1 / -1; }
        .lead-item { background: white; margin: 5px 0; padding: 10px; border-radius: 4px; }
        .high-confidence { border-left: 4px solid #4CAF50; }
        .medium-confidence { border-left: 4px solid #FFC107; }
        .low-confidence { border-left: 4px solid #F44336; }
    </style>
</head>
<body>
    <h1>?? Digital Veteran Dashboard</h1>
    
    <div class="dashboard">
        <div class="card">
            <h3>System Stats</h3>
            <div id="stats">
                <p>Feedback Entries: {{ stats.total_feedback_entries }}</p>
                <p>Evolution Cycles: {{ stats.evolution_cycles }}</p>
                <p>Patterns Learned: {{ stats.patterns_learned }}</p>
            </div>
        </div>
        
        <div class="card">
            <h3>ICP Recommendations</h3>
            <div id="icp">
                <strong>Target:</strong> {{ icp_recs.target_signals|join(', ') }}<br>
                <strong>Avoid:</strong> {{ icp_recs.avoid_signals|join(', ') }}<br>
                <strong>Confidence:</strong> {{ (icp_recs.confidence_level * 100)|round(1) }}%
            </div>
        </div>
        
        <div class="card leads">
            <h3>Generated Leads</h3>
            <button onclick="loadLeads()">Generate New Leads</button>
            <div id="leads-container"></div>
        </div>
    </div>

    <script>
        async function loadLeads() {
            const response = await fetch('/api/leads?count=5');
            const leads = await response.json();
            
            const container = document.getElementById('leads-container');
            container.innerHTML = leads.map(lead => 
                `<div class="lead-item ${getConfidenceClass(lead.confidence_score)}">
                    <strong>${lead.company_name}</strong> - ${lead.industry}<br>
                    Size: ${lead.company_size} | Potential: $${lead.revenue_potential}<br>
                    Confidence: ${(lead.confidence_score * 100).toFixed(1)}%
                </div>`
            ).join('');
        }
        
        function getConfidenceClass(score) {
            if (score > 0.7) return 'high-confidence';
            if (score > 0.5) return 'medium-confidence';
            return 'low-confidence';
        }
        
        // Load initial data
        loadLeads();
    </script>
</body>
</html>
        ''')
    
    print("?? Starting Dashboard on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
