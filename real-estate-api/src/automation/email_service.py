"""
Email Automation Service
Handles all email-related automation workflows
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.models.user import db
from src.models.communication import Communication
from src.models.lead import Lead
from src.models.client import Client

logger = logging.getLogger(__name__)

class EmailService:
    """
    Email automation service for sending automated emails
    """
    
    def __init__(self, smtp_server: str = None, smtp_port: int = 587, 
                 username: str = None, password: str = None):
        self.smtp_server = smtp_server or "smtp.gmail.com"
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.templates = {}
        self._load_default_templates()
        
    def _load_default_templates(self):
        """Load default email templates"""
        self.templates = {
            'welcome_lead': {
                'subject': 'Welcome to {company_name} - Let\'s Find Your Dream Home!',
                'body': '''
Dear {first_name},

Thank you for your interest in working with {company_name}! I'm {agent_name}, and I'm excited to help you with your real estate needs.

Based on your inquiry, I understand you're looking to {property_interest} in the {preferred_areas} area with a budget of ${budget_min:,} - ${budget_max:,}.

Here's what happens next:
1. I'll send you a personalized property search based on your criteria
2. We'll schedule a consultation to discuss your specific needs
3. I'll provide you with market insights and trends for your area of interest

I'm committed to making your real estate journey as smooth as possible. Feel free to reply to this email or call me directly at {agent_phone}.

Best regards,
{agent_name}
{agent_title}
{company_name}
{agent_phone}
{agent_email}
                '''.strip()
            },
            
            'lead_follow_up': {
                'subject': 'Following up on your real estate inquiry - {first_name}',
                'body': '''
Hi {first_name},

I wanted to follow up on your recent inquiry about {property_interest} in {preferred_areas}. 

The market is moving quickly right now, and I've seen some great opportunities that might interest you. I'd love to schedule a brief call to discuss:

• Current market conditions in your area of interest
• New listings that match your criteria
• Financing options and pre-approval process
• Timeline for your real estate goals

When would be a good time for a 15-minute conversation? I'm available:
• Today after 2 PM
• Tomorrow morning between 9 AM - 12 PM
• This weekend by appointment

You can reply to this email or call me directly at {agent_phone}.

Looking forward to helping you achieve your real estate goals!

Best regards,
{agent_name}
{company_name}
{agent_phone}
                '''.strip()
            },
            
            'hot_lead_alert': {
                'subject': 'High-Priority Lead Alert: {first_name} {last_name}',
                'body': '''
URGENT: High-Priority Lead Identified

Lead Details:
• Name: {first_name} {last_name}
• Email: {email}
• Phone: {phone}
• Lead Score: {lead_score}/100
• Source: {lead_source}
• Interest: {property_interest}
• Budget: ${budget_min:,} - ${budget_max:,}
• Timeline: {timeline}

This lead has been identified as high-priority based on our scoring algorithm. 
Recommended action: Contact within 1 hour for best conversion rates.

Lead Notes: {notes}

Take action now in the CRM system.
                '''.strip()
            },
            
            'transaction_milestone_reminder': {
                'subject': 'Transaction Milestone Due: {milestone_name}',
                'body': '''
Dear {agent_name},

This is a reminder that the following transaction milestone is due:

Transaction Details:
• Property: {property_address}
• Client: {client_name}
• Milestone: {milestone_name}
• Due Date: {due_date}
• Status: {milestone_status}

Please ensure this milestone is completed on time to keep the transaction on track.

Transaction Notes: {transaction_notes}

Login to the CRM to update the milestone status.

Best regards,
Real Estate CRM System
                '''.strip()
            },
            
            'daily_report': {
                'subject': 'Daily Real Estate Activity Report - {date}',
                'body': '''
Daily Activity Report for {date}

LEADS:
• New Leads: {new_leads}
• Hot Leads (80+ score): {hot_leads}
• Follow-ups Due: {followups_due}
• Conversions: {conversions}

TRANSACTIONS:
• Active Transactions: {active_transactions}
• Closing This Week: {closing_this_week}
• Overdue Milestones: {overdue_milestones}

MARKETING:
• Active Campaigns: {active_campaigns}
• Email Opens Today: {email_opens}
• New Inquiries: {new_inquiries}

PERFORMANCE:
• Total Pipeline Value: ${pipeline_value:,}
• Projected Monthly Commission: ${projected_commission:,}

Login to your CRM for detailed analytics and next actions.

Have a productive day!
Real Estate CRM System
                '''.strip()
            }
        }
        
    def send_email(self, to_email: str, subject: str, body: str, 
                   from_email: str = None, attachments: List[str] = None) -> bool:
        """Send an email"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email or self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments if any
            if attachments:
                for file_path in attachments:
                    try:
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {file_path.split("/")[-1]}'
                        )
                        msg.attach(part)
                    except Exception as e:
                        logger.error(f"Error attaching file {file_path}: {e}")
            
            # Send email (in production, use real SMTP)
            # For demo purposes, we'll just log the email
            logger.info(f"EMAIL SENT TO: {to_email}")
            logger.info(f"SUBJECT: {subject}")
            logger.info(f"BODY: {body[:200]}...")
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            return False
            
    def send_template_email(self, template_name: str, to_email: str, 
                           variables: Dict[str, Any], from_email: str = None) -> bool:
        """Send an email using a template"""
        if template_name not in self.templates:
            logger.error(f"Template not found: {template_name}")
            return False
            
        template = self.templates[template_name]
        
        try:
            # Format subject and body with variables
            subject = template['subject'].format(**variables)
            body = template['body'].format(**variables)
            
            return self.send_email(to_email, subject, body, from_email)
            
        except KeyError as e:
            logger.error(f"Missing template variable: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending template email: {e}")
            return False
            
    def log_communication(self, user_id: int, to_email: str, subject: str, 
                         body: str, lead_id: int = None, client_id: int = None,
                         campaign_id: int = None, automation_trigger: str = None) -> bool:
        """Log email communication to database"""
        try:
            communication = Communication(
                communication_type='Email',
                direction='Outbound',
                subject=subject,
                content=body,
                status='Sent',
                user_id=user_id,
                lead_id=lead_id,
                client_id=client_id,
                campaign_id=campaign_id,
                is_automated=True,
                automation_trigger=automation_trigger,
                sent_date=datetime.now()
            )
            
            db.session.add(communication)
            db.session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error logging communication: {e}")
            return False

# Email automation workflows
def send_welcome_email(context: Dict[str, Any]) -> bool:
    """Send welcome email to new lead"""
    lead_id = context.get('lead_id')
    if not lead_id:
        return False
        
    lead = Lead.query.get(lead_id)
    if not lead or not lead.assigned_agent:
        return False
        
    agent = lead.assigned_agent
    email_service = EmailService()
    
    variables = {
        'first_name': lead.first_name,
        'company_name': agent.brokerage_name or 'Premier Realty Group',
        'agent_name': f"{agent.first_name} {agent.last_name}",
        'agent_title': agent.role,
        'agent_phone': agent.phone,
        'agent_email': agent.email,
        'property_interest': lead.property_interest or 'buy or sell property',
        'preferred_areas': lead.preferred_areas or 'your preferred areas',
        'budget_min': lead.budget_min or 0,
        'budget_max': lead.budget_max or 0
    }
    
    success = email_service.send_template_email(
        'welcome_lead',
        lead.email,
        variables,
        agent.email
    )
    
    if success:
        email_service.log_communication(
            user_id=agent.id,
            to_email=lead.email,
            subject=f"Welcome to {variables['company_name']}",
            body="Welcome email sent",
            lead_id=lead.id,
            automation_trigger='new_lead'
        )
        
    return success

def send_follow_up_email(context: Dict[str, Any]) -> bool:
    """Send follow-up email to lead"""
    lead_id = context.get('lead_id')
    if not lead_id:
        return False
        
    lead = Lead.query.get(lead_id)
    if not lead or not lead.assigned_agent:
        return False
        
    agent = lead.assigned_agent
    email_service = EmailService()
    
    variables = {
        'first_name': lead.first_name,
        'property_interest': lead.property_interest or 'real estate',
        'preferred_areas': lead.preferred_areas or 'your area of interest',
        'agent_name': f"{agent.first_name} {agent.last_name}",
        'company_name': agent.brokerage_name or 'Premier Realty Group',
        'agent_phone': agent.phone
    }
    
    success = email_service.send_template_email(
        'lead_follow_up',
        lead.email,
        variables,
        agent.email
    )
    
    if success:
        email_service.log_communication(
            user_id=agent.id,
            to_email=lead.email,
            subject=f"Following up on your real estate inquiry",
            body="Follow-up email sent",
            lead_id=lead.id,
            automation_trigger='follow_up_due'
        )
        
    return success

def send_hot_lead_alert(context: Dict[str, Any]) -> bool:
    """Send hot lead alert to agent"""
    lead_id = context.get('lead_id')
    if not lead_id:
        return False
        
    lead = Lead.query.get(lead_id)
    if not lead or not lead.assigned_agent:
        return False
        
    agent = lead.assigned_agent
    email_service = EmailService()
    
    variables = {
        'first_name': lead.first_name,
        'last_name': lead.last_name,
        'email': lead.email,
        'phone': lead.phone,
        'lead_score': lead.lead_score,
        'lead_source': lead.lead_source,
        'property_interest': lead.property_interest,
        'budget_min': lead.budget_min or 0,
        'budget_max': lead.budget_max or 0,
        'timeline': lead.timeline,
        'notes': lead.notes or 'No additional notes'
    }
    
    success = email_service.send_template_email(
        'hot_lead_alert',
        agent.email,
        variables
    )
    
    if success:
        email_service.log_communication(
            user_id=agent.id,
            to_email=agent.email,
            subject=f"High-Priority Lead Alert",
            body="Hot lead alert sent",
            lead_id=lead.id,
            automation_trigger='hot_lead_identified'
        )
        
    return success

# Global email service instance
email_service = EmailService()

