from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    client_type = db.Column(db.String(50), nullable=False)  # Buyer, Seller, Both
    client_status = db.Column(db.String(50), default='Active')
    
    # Preferences
    budget_min = db.Column(db.Float)
    budget_max = db.Column(db.Float)
    preferred_areas = db.Column(db.Text)  # JSON string
    property_types = db.Column(db.Text)  # JSON string
    bedrooms_min = db.Column(db.Integer)
    bathrooms_min = db.Column(db.Float)
    square_feet_min = db.Column(db.Integer)
    special_requirements = db.Column(db.Text)
    
    # Timeline and urgency
    timeline = db.Column(db.String(50))
    pre_approved = db.Column(db.Boolean, default=False)
    pre_approval_amount = db.Column(db.Float)
    lender_info = db.Column(db.Text)
    
    # Contact preferences
    preferred_contact_method = db.Column(db.String(50))
    preferred_contact_time = db.Column(db.String(50))
    communication_frequency = db.Column(db.String(50))
    
    # Additional info
    notes = db.Column(db.Text)
    referral_source = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_contact = db.Column(db.DateTime)
    next_follow_up = db.Column(db.Date)
    
    # Foreign keys
    assigned_agent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    original_lead_id = db.Column(db.Integer)  # Will be linked after lead creation
    
    # Relationships
    assigned_agent = db.relationship('User', backref='clients')
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'client_type': self.client_type,
            'client_status': self.client_status,
            'budget_min': self.budget_min,
            'budget_max': self.budget_max,
            'preferred_areas': self.preferred_areas,
            'property_types': self.property_types,
            'bedrooms_min': self.bedrooms_min,
            'bathrooms_min': self.bathrooms_min,
            'square_feet_min': self.square_feet_min,
            'special_requirements': self.special_requirements,
            'timeline': self.timeline,
            'pre_approved': self.pre_approved,
            'pre_approval_amount': self.pre_approval_amount,
            'lender_info': self.lender_info,
            'preferred_contact_method': self.preferred_contact_method,
            'preferred_contact_time': self.preferred_contact_time,
            'communication_frequency': self.communication_frequency,
            'notes': self.notes,
            'referral_source': self.referral_source,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'last_contact': self.last_contact.isoformat() if self.last_contact else None,
            'next_follow_up': self.next_follow_up.isoformat() if self.next_follow_up else None,
            'assigned_agent_id': self.assigned_agent_id,
            'original_lead_id': self.original_lead_id
        }
    
    def __repr__(self):
        return f'<Client {self.first_name} {self.last_name}>'

