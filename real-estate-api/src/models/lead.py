from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    lead_source = db.Column(db.String(50), nullable=False)
    lead_status = db.Column(db.String(50), default='New')
    lead_score = db.Column(db.Integer, default=0)
    property_interest = db.Column(db.String(50))
    budget_min = db.Column(db.Float)
    budget_max = db.Column(db.Float)
    preferred_areas = db.Column(db.Text)  # JSON string
    timeline = db.Column(db.String(50))
    notes = db.Column(db.Text)
    next_follow_up = db.Column(db.Date)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    assigned_agent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    converted_client_id = db.Column(db.Integer)  # Will be linked after client creation
    source_campaign_id = db.Column(db.Integer)  # Will be linked after campaign creation
    
    # Relationships
    assigned_agent = db.relationship('User', backref='assigned_leads')
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'lead_source': self.lead_source,
            'lead_status': self.lead_status,
            'lead_score': self.lead_score,
            'property_interest': self.property_interest,
            'budget_min': self.budget_min,
            'budget_max': self.budget_max,
            'preferred_areas': self.preferred_areas,
            'timeline': self.timeline,
            'notes': self.notes,
            'next_follow_up': self.next_follow_up.isoformat() if self.next_follow_up else None,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'last_modified': self.last_modified.isoformat() if self.last_modified else None,
            'assigned_agent_id': self.assigned_agent_id,
            'converted_client_id': self.converted_client_id,
            'source_campaign_id': self.source_campaign_id
        }
    
    def __repr__(self):
        return f'<Lead {self.first_name} {self.last_name}>'

