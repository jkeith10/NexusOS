"""
Automation Workflows
Defines all automated workflows for the real estate CRM
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any
from src.models.user import db
from src.models.lead import Lead
from src.models.client import Client
from src.models.transaction import Transaction, TransactionMilestone
from src.models.communication import Communication
from src.models.marketing_campaign import MarketingCampaign
from src.automation.email_service import send_welcome_email, send_follow_up_email, send_hot_lead_alert

logger = logging.getLogger(__name__)

def new_lead_workflow(context: Dict[str, Any]) -> bool:
    """
    Workflow triggered when a new lead is created
    """
    lead_id = context.get('lead_id')
    if not lead_id:
        return False
        
    logger.info(f"Processing new lead workflow for lead {lead_id}")
    
    try:
        lead = Lead.query.get(lead_id)
        if not lead:
            return False
            
        # 1. Send welcome email
        send_welcome_email(context)
        
        # 2. Set next follow-up date
        if not lead.next_follow_up:
            # Follow up in 1 day for hot leads, 3 days for others
            days_to_follow_up = 1 if lead.lead_score >= 80 else 3
            lead.next_follow_up = (datetime.now() + timedelta(days=days_to_follow_up)).date()
            db.session.commit()
            
        # 3. Assign to agent if not already assigned
        if not lead.assigned_agent_id:
            # Simple round-robin assignment (in production, use more sophisticated logic)
            from src.models.user import User
            available_agents = User.query.filter(
                User.role == 'Agent',
                User.status == 'Active'
            ).all()
            
            if available_agents:
                # Assign to agent with least leads
                agent_lead_counts = {}
                for agent in available_agents:
                    count = Lead.query.filter(Lead.assigned_agent_id == agent.id).count()
                    agent_lead_counts[agent.id] = count
                    
                best_agent_id = min(agent_lead_counts, key=agent_lead_counts.get)
                lead.assigned_agent_id = best_agent_id
                db.session.commit()
                
        logger.info(f"New lead workflow completed for lead {lead_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error in new lead workflow: {e}")
        return False

def lead_follow_up_workflow(context: Dict[str, Any]) -> bool:
    """
    Workflow triggered when a lead follow-up is due
    """
    lead_id = context.get('lead_id')
    if not lead_id:
        return False
        
    logger.info(f"Processing follow-up workflow for lead {lead_id}")
    
    try:
        lead = Lead.query.get(lead_id)
        if not lead:
            return False
            
        # Send follow-up email
        send_follow_up_email(context)
        
        # Update next follow-up date based on lead status and score
        if lead.lead_score >= 80:
            # Hot leads - follow up in 2 days
            next_follow_up = datetime.now() + timedelta(days=2)
        elif lead.lead_score >= 60:
            # Warm leads - follow up in 5 days
            next_follow_up = datetime.now() + timedelta(days=5)
        else:
            # Cold leads - follow up in 1 week
            next_follow_up = datetime.now() + timedelta(days=7)
            
        lead.next_follow_up = next_follow_up.date()
        db.session.commit()
        
        logger.info(f"Follow-up workflow completed for lead {lead_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error in follow-up workflow: {e}")
        return False

def hot_lead_workflow(context: Dict[str, Any]) -> bool:
    """
    Workflow triggered when a lead becomes hot (score >= 80)
    """
    lead_id = context.get('lead_id')
    if not lead_id:
        return False
        
    logger.info(f"Processing hot lead workflow for lead {lead_id}")
    
    try:
        lead = Lead.query.get(lead_id)
        if not lead:
            return False
            
        # Send alert to assigned agent
        send_hot_lead_alert(context)
        
        # Update lead status to qualified if not already
        if lead.lead_status in ['New', 'Contacted']:
            lead.lead_status = 'Qualified'
            
        # Set urgent follow-up (within 1 hour)
        lead.next_follow_up = datetime.now().date()
        
        db.session.commit()
        
        logger.info(f"Hot lead workflow completed for lead {lead_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error in hot lead workflow: {e}")
        return False

def transaction_milestone_workflow(context: Dict[str, Any]) -> bool:
    """
    Workflow triggered when a transaction milestone is overdue
    """
    milestone_id = context.get('milestone_id')
    if not milestone_id:
        return False
        
    logger.info(f"Processing milestone workflow for milestone {milestone_id}")
    
    try:
        milestone = TransactionMilestone.query.get(milestone_id)
        if not milestone:
            return False
            
        transaction = Transaction.query.get(milestone.transaction_id)
        if not transaction:
            return False
            
        # Send reminder to listing agent
        if transaction.listing_agent:
            from src.automation.email_service import EmailService
            email_service = EmailService()
            
            variables = {
                'agent_name': f"{transaction.listing_agent.first_name} {transaction.listing_agent.last_name}",
                'milestone_name': milestone.milestone_name,
                'due_date': milestone.due_date.strftime('%Y-%m-%d') if milestone.due_date else 'Not set',
                'milestone_status': milestone.milestone_status,
                'property_address': f"{transaction.property.address}" if transaction.property else 'Unknown',
                'client_name': f"{transaction.client.first_name} {transaction.client.last_name}" if transaction.client else 'Unknown',
                'transaction_notes': transaction.notes or 'No notes'
            }
            
            email_service.send_template_email(
                'transaction_milestone_reminder',
                transaction.listing_agent.email,
                variables
            )
            
        # Update milestone status to overdue if still pending
        if milestone.milestone_status == 'Pending':
            milestone.milestone_status = 'Overdue'
            
        # Increase transaction risk score
        if transaction.risk_score < 100:
            transaction.risk_score = min(transaction.risk_score + 10, 100)
            
            # Update risk level based on score
            if transaction.risk_score >= 70:
                transaction.risk_level = 'High'
            elif transaction.risk_score >= 40:
                transaction.risk_level = 'Medium'
            else:
                transaction.risk_level = 'Low'
                
        db.session.commit()
        
        logger.info(f"Milestone workflow completed for milestone {milestone_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error in milestone workflow: {e}")
        return False

def daily_report_workflow(context: Dict[str, Any]) -> bool:
    """
    Generate and send daily activity reports
    """
    report_date = context.get('date', datetime.now().date())
    
    logger.info(f"Generating daily report for {report_date}")
    
    try:
        # Calculate metrics
        today_start = datetime.combine(report_date, datetime.min.time())
        today_end = datetime.combine(report_date, datetime.max.time())
        
        # Lead metrics
        new_leads = Lead.query.filter(
            Lead.created_date >= today_start,
            Lead.created_date <= today_end
        ).count()
        
        hot_leads = Lead.query.filter(Lead.lead_score >= 80).count()
        
        followups_due = Lead.query.filter(
            Lead.next_follow_up <= report_date,
            Lead.lead_status.in_(['New', 'Contacted', 'Qualified', 'Nurturing'])
        ).count()
        
        conversions = Lead.query.filter(
            Lead.lead_status == 'Converted',
            Lead.last_modified >= today_start,
            Lead.last_modified <= today_end
        ).count()
        
        # Transaction metrics
        active_transactions = Transaction.query.filter(
            Transaction.transaction_status.in_(['Active', 'Under Contract', 'Pending'])
        ).count()
        
        week_end = report_date + timedelta(days=7)
        closing_this_week = Transaction.query.filter(
            Transaction.closing_date.between(report_date, week_end),
            Transaction.transaction_status != 'Closed'
        ).count()
        
        overdue_milestones = TransactionMilestone.query.filter(
            TransactionMilestone.due_date < report_date,
            TransactionMilestone.milestone_status.in_(['Pending', 'In Progress'])
        ).count()
        
        # Marketing metrics
        active_campaigns = MarketingCampaign.query.filter(
            MarketingCampaign.campaign_status == 'Active'
        ).count()
        
        email_opens = Communication.query.filter(
            Communication.communication_type == 'Email',
            Communication.sent_date >= today_start,
            Communication.sent_date <= today_end,
            Communication.opened == True
        ).count()
        
        new_inquiries = Lead.query.filter(
            Lead.created_date >= today_start,
            Lead.created_date <= today_end
        ).count()
        
        # Performance metrics
        pipeline_value = db.session.query(db.func.sum(Transaction.sale_price)).filter(
            Transaction.transaction_status.in_(['Active', 'Under Contract', 'Pending'])
        ).scalar() or 0
        
        projected_commission = db.session.query(db.func.sum(Transaction.total_commission)).filter(
            Transaction.transaction_status.in_(['Active', 'Under Contract', 'Pending'])
        ).scalar() or 0
        
        # Send report to all active agents
        from src.models.user import User
        from src.automation.email_service import EmailService
        
        agents = User.query.filter(
            User.role == 'Agent',
            User.status == 'Active'
        ).all()
        
        email_service = EmailService()
        
        variables = {
            'date': report_date.strftime('%Y-%m-%d'),
            'new_leads': new_leads,
            'hot_leads': hot_leads,
            'followups_due': followups_due,
            'conversions': conversions,
            'active_transactions': active_transactions,
            'closing_this_week': closing_this_week,
            'overdue_milestones': overdue_milestones,
            'active_campaigns': active_campaigns,
            'email_opens': email_opens,
            'new_inquiries': new_inquiries,
            'pipeline_value': pipeline_value,
            'projected_commission': projected_commission
        }
        
        for agent in agents:
            email_service.send_template_email(
                'daily_report',
                agent.email,
                variables
            )
            
        logger.info(f"Daily report sent to {len(agents)} agents")
        return True
        
    except Exception as e:
        logger.error(f"Error generating daily report: {e}")
        return False

def campaign_completed_workflow(context: Dict[str, Any]) -> bool:
    """
    Workflow triggered when a marketing campaign is completed
    """
    campaign_id = context.get('campaign_id')
    if not campaign_id:
        return False
        
    logger.info(f"Processing campaign completion workflow for campaign {campaign_id}")
    
    try:
        campaign = MarketingCampaign.query.get(campaign_id)
        if not campaign:
            return False
            
        # Calculate final ROI
        if campaign.budget and campaign.budget > 0:
            # Simplified ROI calculation based on leads generated
            estimated_revenue = campaign.leads_generated * 5000  # Assume $5k average commission per lead
            campaign.roi = (estimated_revenue - campaign.budget) / campaign.budget
            
        # Update cost per lead
        if campaign.leads_generated > 0:
            campaign.cost_per_lead = campaign.budget / campaign.leads_generated
            
        db.session.commit()
        
        # Send completion report to campaign creator
        if campaign.created_by:
            from src.automation.email_service import EmailService
            email_service = EmailService()
            
            subject = f"Campaign Completed: {campaign.campaign_name}"
            body = f"""
Campaign "{campaign.campaign_name}" has been completed.

Final Results:
• Leads Generated: {campaign.leads_generated}
• Cost Per Lead: ${campaign.cost_per_lead:.2f}
• ROI: {campaign.roi:.1%}
• Total Budget: ${campaign.budget}

Campaign ran from {campaign.start_date} to {campaign.end_date}.

Login to the CRM for detailed analytics.
            """.strip()
            
            email_service.send_email(
                campaign.created_by.email,
                subject,
                body
            )
            
        logger.info(f"Campaign completion workflow finished for campaign {campaign_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error in campaign completion workflow: {e}")
        return False

# Workflow registry - maps workflow names to functions
WORKFLOWS = {
    'new_lead': new_lead_workflow,
    'lead_follow_up': lead_follow_up_workflow,
    'hot_lead_identified': hot_lead_workflow,
    'milestone_overdue': transaction_milestone_workflow,
    'daily_report_generation': daily_report_workflow,
    'campaign_completed': campaign_completed_workflow
}

# Trigger conditions
def new_lead_trigger(data: Dict[str, Any]) -> bool:
    """Trigger condition for new leads"""
    return data.get('event') == 'lead_created'

def follow_up_due_trigger(data: Dict[str, Any]) -> bool:
    """Trigger condition for follow-up due"""
    return data.get('lead_id') is not None

def hot_lead_trigger(data: Dict[str, Any]) -> bool:
    """Trigger condition for hot leads"""
    return data.get('score', 0) >= 80

def milestone_overdue_trigger(data: Dict[str, Any]) -> bool:
    """Trigger condition for overdue milestones"""
    return data.get('milestone_id') is not None

def daily_report_trigger(data: Dict[str, Any]) -> bool:
    """Trigger condition for daily reports"""
    return data.get('date') is not None

def campaign_completed_trigger(data: Dict[str, Any]) -> bool:
    """Trigger condition for completed campaigns"""
    return data.get('campaign_id') is not None

# Trigger registry
TRIGGERS = {
    'new_lead': new_lead_trigger,
    'lead_follow_up_due': follow_up_due_trigger,
    'hot_lead_identified': hot_lead_trigger,
    'milestone_overdue': milestone_overdue_trigger,
    'daily_report': daily_report_trigger,
    'campaign_completed': campaign_completed_trigger
}

