"""
Automation API Routes
Provides endpoints for managing and monitoring automation workflows
"""
from flask import Blueprint, request, jsonify
from src.automation.engine import automation_engine
from src.automation.workflows import WORKFLOWS, TRIGGERS
import logging

logger = logging.getLogger(__name__)

automation_bp = Blueprint('automation', __name__)

@automation_bp.route('/automation/status', methods=['GET'])
def get_automation_status():
    """Get automation engine status"""
    try:
        status = automation_engine.get_status()
        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@automation_bp.route('/automation/start', methods=['POST'])
def start_automation():
    """Start the automation engine"""
    try:
        automation_engine.start()
        return jsonify({
            'success': True,
            'message': 'Automation engine started'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@automation_bp.route('/automation/stop', methods=['POST'])
def stop_automation():
    """Stop the automation engine"""
    try:
        automation_engine.stop()
        return jsonify({
            'success': True,
            'message': 'Automation engine stopped'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@automation_bp.route('/automation/workflows', methods=['GET'])
def list_workflows():
    """List all available workflows"""
    try:
        workflows = list(WORKFLOWS.keys())
        return jsonify({
            'success': True,
            'workflows': workflows,
            'count': len(workflows)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@automation_bp.route('/automation/workflows/<workflow_name>/execute', methods=['POST'])
def execute_workflow(workflow_name):
    """Execute a specific workflow manually"""
    try:
        data = request.get_json() or {}
        
        if workflow_name not in WORKFLOWS:
            return jsonify({
                'success': False,
                'error': f'Workflow not found: {workflow_name}'
            }), 404
            
        result = automation_engine.execute_workflow(workflow_name, data)
        
        return jsonify({
            'success': True,
            'workflow': workflow_name,
            'result': result,
            'message': f'Workflow {workflow_name} executed'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@automation_bp.route('/automation/triggers/<trigger_name>', methods=['POST'])
def trigger_workflow(trigger_name):
    """Trigger workflows based on events"""
    try:
        data = request.get_json() or {}
        
        if trigger_name not in TRIGGERS:
            return jsonify({
                'success': False,
                'error': f'Trigger not found: {trigger_name}'
            }), 404
            
        automation_engine.trigger_workflow(trigger_name, data)
        
        return jsonify({
            'success': True,
            'trigger': trigger_name,
            'message': f'Trigger {trigger_name} processed'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@automation_bp.route('/automation/test/new-lead', methods=['POST'])
def test_new_lead_automation():
    """Test the new lead automation workflow"""
    try:
        data = request.get_json()
        lead_id = data.get('lead_id')
        
        if not lead_id:
            return jsonify({
                'success': False,
                'error': 'lead_id is required'
            }), 400
            
        # Trigger new lead workflow
        result = automation_engine.execute_workflow('new_lead', {'lead_id': lead_id})
        
        return jsonify({
            'success': True,
            'result': result,
            'message': f'New lead automation tested for lead {lead_id}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@automation_bp.route('/automation/test/follow-up', methods=['POST'])
def test_follow_up_automation():
    """Test the follow-up automation workflow"""
    try:
        data = request.get_json()
        lead_id = data.get('lead_id')
        
        if not lead_id:
            return jsonify({
                'success': False,
                'error': 'lead_id is required'
            }), 400
            
        # Trigger follow-up workflow
        result = automation_engine.execute_workflow('lead_follow_up', {'lead_id': lead_id})
        
        return jsonify({
            'success': True,
            'result': result,
            'message': f'Follow-up automation tested for lead {lead_id}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@automation_bp.route('/automation/test/hot-lead', methods=['POST'])
def test_hot_lead_automation():
    """Test the hot lead automation workflow"""
    try:
        data = request.get_json()
        lead_id = data.get('lead_id')
        
        if not lead_id:
            return jsonify({
                'success': False,
                'error': 'lead_id is required'
            }), 400
            
        # Trigger hot lead workflow
        result = automation_engine.execute_workflow('hot_lead_identified', {
            'lead_id': lead_id,
            'score': 85
        })
        
        return jsonify({
            'success': True,
            'result': result,
            'message': f'Hot lead automation tested for lead {lead_id}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@automation_bp.route('/automation/test/daily-report', methods=['POST'])
def test_daily_report_automation():
    """Test the daily report automation"""
    try:
        from datetime import datetime
        
        # Trigger daily report workflow
        result = automation_engine.execute_workflow('daily_report_generation', {
            'date': datetime.now().date()
        })
        
        return jsonify({
            'success': True,
            'result': result,
            'message': 'Daily report automation tested'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@automation_bp.route('/automation/metrics', methods=['GET'])
def get_automation_metrics():
    """Get automation performance metrics"""
    try:
        from src.models.communication import Communication
        from datetime import datetime, timedelta
        
        # Get automation statistics
        week_ago = datetime.now() - timedelta(days=7)
        
        automated_emails = Communication.query.filter(
            Communication.is_automated == True,
            Communication.communication_type == 'Email',
            Communication.sent_date >= week_ago
        ).count()
        
        total_communications = Communication.query.filter(
            Communication.sent_date >= week_ago
        ).count()
        
        automation_rate = (automated_emails / total_communications * 100) if total_communications > 0 else 0
        
        # Get workflow execution stats
        status = automation_engine.get_status()
        
        metrics = {
            'automation_rate': round(automation_rate, 1),
            'automated_emails_week': automated_emails,
            'total_communications_week': total_communications,
            'workflows_registered': status['workflows_registered'],
            'triggers_registered': status['triggers_registered'],
            'engine_running': status['running'],
            'workflow_stats': status['workflows']
        }
        
        return jsonify({
            'success': True,
            'metrics': metrics
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

