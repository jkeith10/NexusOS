from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class MarketingCampaign(db.Model):
    __tablename__ = 'marketing_campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Campaign basics
    campaign_name = db.Column(db.String(255), nullable=False)
    campaign_type = db.Column(db.String(50), nullable=False)  # Email, SMS, Social, PPC, Direct Mail
    campaign_status = db.Column(db.String(50), default='Draft')  # Draft, Active, Paused, Completed
    
    # Campaign details
    description = db.Column(db.Text)
    target_audience = db.Column(db.String(100))  # Buyers, Sellers, Investors, etc.
    budget = db.Column(db.Float)
    
    # Dates
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Performance metrics
    impressions = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    conversions = db.Column(db.Integer, default=0)
    leads_generated = db.Column(db.Integer, default=0)
    cost_per_lead = db.Column(db.Float)
    roi = db.Column(db.Float)
    
    # Email specific metrics
    emails_sent = db.Column(db.Integer, default=0)
    emails_delivered = db.Column(db.Integer, default=0)
    emails_opened = db.Column(db.Integer, default=0)
    emails_clicked = db.Column(db.Integer, default=0)
    unsubscribes = db.Column(db.Integer, default=0)
    
    # SMS specific metrics
    sms_sent = db.Column(db.Integer, default=0)
    sms_delivered = db.Column(db.Integer, default=0)
    sms_replied = db.Column(db.Integer, default=0)
    
    # Social media metrics
    social_posts = db.Column(db.Integer, default=0)
    social_engagement = db.Column(db.Integer, default=0)
    social_shares = db.Column(db.Integer, default=0)
    
    # Campaign content
    email_template = db.Column(db.Text)
    sms_template = db.Column(db.Text)
    social_content = db.Column(db.Text)
    
    # Automation settings
    is_automated = db.Column(db.Boolean, default=False)
    automation_trigger = db.Column(db.String(100))
    automation_frequency = db.Column(db.String(50))
    
    # Targeting criteria (JSON strings)
    geographic_targeting = db.Column(db.Text)
    demographic_targeting = db.Column(db.Text)
    behavioral_targeting = db.Column(db.Text)
    
    # Foreign keys
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))  # For property-specific campaigns
    
    # Relationships
    created_by = db.relationship('User', backref='created_campaigns')
    
    def to_dict(self):
        return {
            'id': self.id,
            'campaign_name': self.campaign_name,
            'campaign_type': self.campaign_type,
            'campaign_status': self.campaign_status,
            'description': self.description,
            'target_audience': self.target_audience,
            'budget': self.budget,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'impressions': self.impressions,
            'clicks': self.clicks,
            'conversions': self.conversions,
            'leads_generated': self.leads_generated,
            'cost_per_lead': self.cost_per_lead,
            'roi': self.roi,
            'emails_sent': self.emails_sent,
            'emails_delivered': self.emails_delivered,
            'emails_opened': self.emails_opened,
            'emails_clicked': self.emails_clicked,
            'unsubscribes': self.unsubscribes,
            'sms_sent': self.sms_sent,
            'sms_delivered': self.sms_delivered,
            'sms_replied': self.sms_replied,
            'social_posts': self.social_posts,
            'social_engagement': self.social_engagement,
            'social_shares': self.social_shares,
            'email_template': self.email_template,
            'sms_template': self.sms_template,
            'social_content': self.social_content,
            'is_automated': self.is_automated,
            'automation_trigger': self.automation_trigger,
            'automation_frequency': self.automation_frequency,
            'geographic_targeting': self.geographic_targeting,
            'demographic_targeting': self.demographic_targeting,
            'behavioral_targeting': self.behavioral_targeting,
            'created_by_id': self.created_by_id,
            'property_id': self.property_id
        }
    
    def __repr__(self):
        return f'<MarketingCampaign {self.campaign_name}>'

