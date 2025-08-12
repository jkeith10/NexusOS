from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic user info
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    
    # Authentication
    password_hash = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    
    # Real estate agent specific fields
    role = db.Column(db.String(50), default='Agent')  # Agent, Broker, Assistant, Manager
    license_number = db.Column(db.String(50))
    license_state = db.Column(db.String(50))
    license_expiry = db.Column(db.Date)
    
    # Territory and specialization
    territory = db.Column(db.Text)  # JSON string of areas
    specializations = db.Column(db.Text)  # JSON string of property types/markets
    
    # Performance metrics
    ytd_transactions = db.Column(db.Integer, default=0)
    ytd_volume = db.Column(db.Float, default=0.0)
    ytd_commission = db.Column(db.Float, default=0.0)
    commission_rate = db.Column(db.Float, default=0.03)  # 3% default
    
    # Contact preferences
    preferred_contact_method = db.Column(db.String(50), default='Email')
    work_hours_start = db.Column(db.Time)
    work_hours_end = db.Column(db.Time)
    time_zone = db.Column(db.String(50))
    
    # Profile information
    bio = db.Column(db.Text)
    profile_photo_url = db.Column(db.String(500))
    website_url = db.Column(db.String(500))
    social_media_links = db.Column(db.Text)  # JSON string
    
    # System fields
    hire_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='Active')  # Active, Inactive, On Leave
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Team/Brokerage info
    team_id = db.Column(db.Integer)  # For future team functionality
    brokerage_name = db.Column(db.String(255))
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    manager = db.relationship('User', remote_side=[id], backref='team_members')
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'is_active': self.is_active,
            'role': self.role,
            'license_number': self.license_number,
            'license_state': self.license_state,
            'license_expiry': self.license_expiry.isoformat() if self.license_expiry else None,
            'territory': self.territory,
            'specializations': self.specializations,
            'ytd_transactions': self.ytd_transactions,
            'ytd_volume': self.ytd_volume,
            'ytd_commission': self.ytd_commission,
            'commission_rate': self.commission_rate,
            'preferred_contact_method': self.preferred_contact_method,
            'work_hours_start': self.work_hours_start.isoformat() if self.work_hours_start else None,
            'work_hours_end': self.work_hours_end.isoformat() if self.work_hours_end else None,
            'time_zone': self.time_zone,
            'bio': self.bio,
            'profile_photo_url': self.profile_photo_url,
            'website_url': self.website_url,
            'social_media_links': self.social_media_links,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'status': self.status,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'team_id': self.team_id,
            'brokerage_name': self.brokerage_name,
            'manager_id': self.manager_id
        }
    
    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'
