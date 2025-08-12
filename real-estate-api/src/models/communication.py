from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Communication(db.Model):
    __tablename__ = 'communications'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Communication details
    communication_type = db.Column(db.String(50), nullable=False)  # Email, SMS, Call, Meeting, Note
    direction = db.Column(db.String(20), nullable=False)  # Inbound, Outbound
    subject = db.Column(db.String(255))
    content = db.Column(db.Text)
    
    # Status and tracking
    status = db.Column(db.String(50), default='Sent')  # Sent, Delivered, Read, Responded, Failed
    priority = db.Column(db.String(20), default='Normal')  # Low, Normal, High, Urgent
    
    # Timestamps
    sent_date = db.Column(db.DateTime, default=datetime.utcnow)
    delivered_date = db.Column(db.DateTime)
    read_date = db.Column(db.DateTime)
    response_date = db.Column(db.DateTime)
    
    # Automation fields
    is_automated = db.Column(db.Boolean, default=False)
    automation_trigger = db.Column(db.String(100))  # What triggered this communication
    follow_up_required = db.Column(db.Boolean, default=False)
    follow_up_date = db.Column(db.DateTime)
    
    # Engagement tracking
    opened = db.Column(db.Boolean, default=False)
    clicked = db.Column(db.Boolean, default=False)
    replied = db.Column(db.Boolean, default=False)
    
    # Additional metadata
    external_id = db.Column(db.String(100))  # ID from email/SMS provider
    cost = db.Column(db.Float)  # Cost of SMS or other paid communication
    notes = db.Column(db.Text)
    
    # Foreign keys - flexible contact system
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Who sent/received
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('marketing_campaigns.id'))
    
    # Relationships
    user = db.relationship('User', backref='communications')
    campaign = db.relationship('MarketingCampaign', backref='campaign_communications')
    
    def to_dict(self):
        return {
            'id': self.id,
            'communication_type': self.communication_type,
            'direction': self.direction,
            'subject': self.subject,
            'content': self.content,
            'status': self.status,
            'priority': self.priority,
            'sent_date': self.sent_date.isoformat() if self.sent_date else None,
            'delivered_date': self.delivered_date.isoformat() if self.delivered_date else None,
            'read_date': self.read_date.isoformat() if self.read_date else None,
            'response_date': self.response_date.isoformat() if self.response_date else None,
            'is_automated': self.is_automated,
            'automation_trigger': self.automation_trigger,
            'follow_up_required': self.follow_up_required,
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None,
            'opened': self.opened,
            'clicked': self.clicked,
            'replied': self.replied,
            'external_id': self.external_id,
            'cost': self.cost,
            'notes': self.notes,
            'user_id': self.user_id,
            'lead_id': self.lead_id,
            'client_id': self.client_id,
            'transaction_id': self.transaction_id,
            'campaign_id': self.campaign_id
        }
    
    def __repr__(self):
        return f'<Communication {self.communication_type} - {self.subject}>'

