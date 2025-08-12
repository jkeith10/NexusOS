"""
Core Automation Engine for Real Estate CRM
Replaces Make.com functionality with built-in automation workflows
"""
import threading
import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, List, Any, Callable
import logging
from src.models.user import db
from src.models.lead import Lead
from src.models.client import Client
from src.models.transaction import Transaction, TransactionMilestone
from src.models.communication import Communication
from src.models.marketing_campaign import MarketingCampaign

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutomationEngine:
    """
    Central automation engine that manages all automated workflows
    """
    
    def __init__(self, app=None):
        self.app = app
        self.workflows = {}
        self.triggers = {}
        self.running = False
        self.scheduler_thread = None
        
    def init_app(self, app):
        """Initialize with Flask app context"""
        self.app = app
        
    def register_workflow(self, name: str, workflow_func: Callable, trigger_type: str = 'manual'):
        """Register a new automation workflow"""
        self.workflows[name] = {
            'function': workflow_func,
            'trigger_type': trigger_type,
            'last_run': None,
            'run_count': 0
        }
        logger.info(f"Registered workflow: {name}")
        
    def register_trigger(self, trigger_name: str, condition_func: Callable, workflow_name: str):
        """Register a trigger condition for a workflow"""
        if trigger_name not in self.triggers:
            self.triggers[trigger_name] = []
        
        self.triggers[trigger_name].append({
            'condition': condition_func,
            'workflow': workflow_name
        })
        logger.info(f"Registered trigger: {trigger_name} -> {workflow_name}")
        
    def start(self):
        """Start the automation engine"""
        if self.running:
            return
            
        self.running = True
        logger.info("Starting Automation Engine...")
        
        # Schedule periodic tasks
        schedule.every(5).minutes.do(self._check_lead_follow_ups)
        schedule.every(10).minutes.do(self._check_transaction_milestones)
        schedule.every(30).minutes.do(self._process_lead_scoring)
        schedule.every(1).hours.do(self._check_marketing_campaigns)
        schedule.every(1).days.do(self._daily_maintenance)
        
        # Start scheduler thread
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("Automation Engine started successfully")
        
    def stop(self):
        """Stop the automation engine"""
        self.running = False
        logger.info("Automation Engine stopped")
        
    def _run_scheduler(self):
        """Run the scheduler in a separate thread"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(60)
                
    def execute_workflow(self, workflow_name: str, context: Dict[str, Any] = None):
        """Execute a specific workflow"""
        if workflow_name not in self.workflows:
            logger.error(f"Workflow not found: {workflow_name}")
            return False
            
        try:
            with self.app.app_context():
                workflow = self.workflows[workflow_name]
                result = workflow['function'](context or {})
                
                # Update workflow stats
                workflow['last_run'] = datetime.now()
                workflow['run_count'] += 1
                
                logger.info(f"Executed workflow: {workflow_name}")
                return result
                
        except Exception as e:
            logger.error(f"Error executing workflow {workflow_name}: {e}")
            return False
            
    def trigger_workflow(self, trigger_name: str, data: Dict[str, Any] = None):
        """Trigger workflows based on events"""
        if trigger_name not in self.triggers:
            return
            
        for trigger in self.triggers[trigger_name]:
            try:
                if trigger['condition'](data or {}):
                    self.execute_workflow(trigger['workflow'], data)
            except Exception as e:
                logger.error(f"Error in trigger {trigger_name}: {e}")
                
    def _check_lead_follow_ups(self):
        """Check for leads that need follow-up"""
        logger.info("Checking lead follow-ups...")
        
        with self.app.app_context():
            # Get leads that need follow-up
            overdue_leads = Lead.query.filter(
                Lead.next_follow_up <= datetime.now().date(),
                Lead.lead_status.in_(['New', 'Contacted', 'Qualified', 'Nurturing'])
            ).all()
            
            for lead in overdue_leads:
                self.trigger_workflow('lead_follow_up_due', {
                    'lead_id': lead.id,
                    'lead': lead,
                    'days_overdue': (datetime.now().date() - lead.next_follow_up).days
                })
                
    def _check_transaction_milestones(self):
        """Check for transaction milestones that are due or overdue"""
        logger.info("Checking transaction milestones...")
        
        with self.app.app_context():
            # Get overdue milestones
            overdue_milestones = TransactionMilestone.query.filter(
                TransactionMilestone.due_date <= datetime.now().date(),
                TransactionMilestone.milestone_status.in_(['Pending', 'In Progress'])
            ).all()
            
            for milestone in overdue_milestones:
                self.trigger_workflow('milestone_overdue', {
                    'milestone_id': milestone.id,
                    'milestone': milestone,
                    'transaction_id': milestone.transaction_id
                })
                
    def _process_lead_scoring(self):
        """Recalculate lead scores and trigger actions for high-scoring leads"""
        logger.info("Processing lead scoring...")
        
        with self.app.app_context():
            # Get all active leads
            active_leads = Lead.query.filter(
                Lead.lead_status.in_(['New', 'Contacted', 'Qualified', 'Nurturing'])
            ).all()
            
            for lead in active_leads:
                # Recalculate score (simplified version)
                old_score = lead.lead_score
                new_score = self._calculate_lead_score(lead)
                
                if new_score != old_score:
                    lead.lead_score = new_score
                    db.session.commit()
                    
                    # Trigger actions for high-scoring leads
                    if new_score >= 80 and old_score < 80:
                        self.trigger_workflow('hot_lead_identified', {
                            'lead_id': lead.id,
                            'lead': lead,
                            'score': new_score
                        })
                        
    def _check_marketing_campaigns(self):
        """Check and update marketing campaign status"""
        logger.info("Checking marketing campaigns...")
        
        with self.app.app_context():
            # Get active campaigns
            active_campaigns = MarketingCampaign.query.filter(
                MarketingCampaign.campaign_status == 'Active'
            ).all()
            
            for campaign in active_campaigns:
                # Check if campaign should end
                if campaign.end_date and campaign.end_date <= datetime.now().date():
                    campaign.campaign_status = 'Completed'
                    db.session.commit()
                    
                    self.trigger_workflow('campaign_completed', {
                        'campaign_id': campaign.id,
                        'campaign': campaign
                    })
                    
    def _daily_maintenance(self):
        """Perform daily maintenance tasks"""
        logger.info("Running daily maintenance...")
        
        with self.app.app_context():
            # Update lead statuses based on inactivity
            inactive_threshold = datetime.now() - timedelta(days=30)
            
            inactive_leads = Lead.query.filter(
                Lead.last_modified < inactive_threshold,
                Lead.lead_status.in_(['New', 'Contacted', 'Nurturing'])
            ).all()
            
            for lead in inactive_leads:
                lead.lead_status = 'Unresponsive'
                
            db.session.commit()
            
            # Generate daily reports
            self.trigger_workflow('daily_report_generation', {
                'date': datetime.now().date()
            })
            
    def _calculate_lead_score(self, lead: Lead) -> int:
        """Calculate lead score based on various factors"""
        score = 0
        
        # Source scoring
        source_scores = {
            'Referral': 30,
            'Website Form': 25,
            'Google Ads': 20,
            'Social Media': 18,
            'Open House': 15,
            'Zillow': 12,
            'Realtor.com': 10,
            'Cold Call': 8,
            'Other': 5
        }
        score += source_scores.get(lead.lead_source, 5)
        
        # Timeline scoring
        timeline_scores = {
            'ASAP': 25,
            '1-3 months': 20,
            '3-6 months': 15,
            '6-12 months': 10,
            '1+ years': 5,
            'Just browsing': 3
        }
        score += timeline_scores.get(lead.timeline, 3)
        
        # Budget scoring
        if lead.budget_max:
            if lead.budget_max >= 1000000:
                score += 20
            elif lead.budget_max >= 500000:
                score += 15
            elif lead.budget_max >= 300000:
                score += 10
            elif lead.budget_max >= 200000:
                score += 8
            else:
                score += 5
                
        # Property interest scoring
        interest_scores = {
            'Buying': 15,
            'Both': 12,
            'Selling': 10,
            'Investing': 8,
            'Renting': 3
        }
        score += interest_scores.get(lead.property_interest, 5)
        
        # Contact completeness
        if lead.email:
            score += 5
        if lead.phone:
            score += 5
            
        # Engagement scoring (based on communications)
        recent_communications = Communication.query.filter(
            Communication.lead_id == lead.id,
            Communication.sent_date >= datetime.now() - timedelta(days=7)
        ).count()
        
        score += min(recent_communications * 2, 10)  # Max 10 points for engagement
        
        return min(score, 100)  # Cap at 100
        
    def get_status(self) -> Dict[str, Any]:
        """Get automation engine status"""
        return {
            'running': self.running,
            'workflows_registered': len(self.workflows),
            'triggers_registered': sum(len(triggers) for triggers in self.triggers.values()),
            'workflows': {
                name: {
                    'last_run': workflow['last_run'].isoformat() if workflow['last_run'] else None,
                    'run_count': workflow['run_count']
                }
                for name, workflow in self.workflows.items()
            }
        }

# Global automation engine instance
automation_engine = AutomationEngine()

