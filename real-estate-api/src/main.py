import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.lead import Lead
from src.models.client import Client
from src.models.property import Property
from src.models.transaction import Transaction, TransactionMilestone, TransactionDocument
from src.models.communication import Communication
from src.models.marketing_campaign import MarketingCampaign
from src.routes.user import user_bp
from src.routes.transaction import transaction_bp
from src.routes.lead import lead_bp
from src.routes.automation import automation_bp
from src.automation.engine import automation_engine
from src.automation.workflows import WORKFLOWS, TRIGGERS

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(transaction_bp, url_prefix='/api')
app.register_blueprint(lead_bp, url_prefix='/api')
app.register_blueprint(automation_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize automation engine
automation_engine.init_app(app)

# Create all tables
with app.app_context():
    db.create_all()
    
    # Register automation workflows
    for workflow_name, workflow_func in WORKFLOWS.items():
        automation_engine.register_workflow(workflow_name, workflow_func)
    
    # Register automation triggers
    automation_engine.register_trigger('new_lead', TRIGGERS['new_lead'], 'new_lead')
    automation_engine.register_trigger('lead_follow_up_due', TRIGGERS['lead_follow_up_due'], 'lead_follow_up')
    automation_engine.register_trigger('hot_lead_identified', TRIGGERS['hot_lead_identified'], 'hot_lead_identified')
    automation_engine.register_trigger('milestone_overdue', TRIGGERS['milestone_overdue'], 'milestone_overdue')
    automation_engine.register_trigger('daily_report', TRIGGERS['daily_report'], 'daily_report_generation')
    automation_engine.register_trigger('campaign_completed', TRIGGERS['campaign_completed'], 'campaign_completed')
    
    # Start automation engine
    automation_engine.start()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
