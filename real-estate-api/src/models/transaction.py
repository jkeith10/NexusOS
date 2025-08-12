from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic transaction info
    transaction_type = db.Column(db.String(50), nullable=False)  # Purchase, Sale, Lease
    transaction_status = db.Column(db.String(50), default='Active')
    
    # Key dates
    contract_date = db.Column(db.Date)
    closing_date = db.Column(db.Date)
    actual_closing_date = db.Column(db.Date)
    inspection_date = db.Column(db.Date)
    appraisal_date = db.Column(db.Date)
    
    # Financial details
    sale_price = db.Column(db.Float)
    earnest_money = db.Column(db.Float)
    down_payment = db.Column(db.Float)
    loan_amount = db.Column(db.Float)
    
    # Commission information
    commission_rate = db.Column(db.Float)
    total_commission = db.Column(db.Float)
    listing_commission = db.Column(db.Float)
    buyer_commission = db.Column(db.Float)
    
    # Progress tracking
    progress_percentage = db.Column(db.Integer, default=0)
    current_milestone = db.Column(db.String(100))
    
    # Risk assessment
    risk_score = db.Column(db.Integer, default=0)
    risk_level = db.Column(db.String(20), default='Low')  # Low, Medium, High
    risk_factors = db.Column(db.Text)  # JSON string
    
    # Additional information
    notes = db.Column(db.Text)
    special_conditions = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    listing_agent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    buyer_agent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    listing_agent = db.relationship('User', foreign_keys=[listing_agent_id], backref='listing_transactions')
    buyer_agent = db.relationship('User', foreign_keys=[buyer_agent_id], backref='buyer_transactions')
    milestones = db.relationship('TransactionMilestone', backref='transaction', cascade='all, delete-orphan')
    documents = db.relationship('TransactionDocument', backref='transaction', cascade='all, delete-orphan')
    communications = db.relationship('Communication', backref='transaction_related')
    
    def to_dict(self):
        return {
            'id': self.id,
            'transaction_type': self.transaction_type,
            'transaction_status': self.transaction_status,
            'contract_date': self.contract_date.isoformat() if self.contract_date else None,
            'closing_date': self.closing_date.isoformat() if self.closing_date else None,
            'actual_closing_date': self.actual_closing_date.isoformat() if self.actual_closing_date else None,
            'inspection_date': self.inspection_date.isoformat() if self.inspection_date else None,
            'appraisal_date': self.appraisal_date.isoformat() if self.appraisal_date else None,
            'sale_price': self.sale_price,
            'earnest_money': self.earnest_money,
            'down_payment': self.down_payment,
            'loan_amount': self.loan_amount,
            'commission_rate': self.commission_rate,
            'total_commission': self.total_commission,
            'listing_commission': self.listing_commission,
            'buyer_commission': self.buyer_commission,
            'progress_percentage': self.progress_percentage,
            'current_milestone': self.current_milestone,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level,
            'risk_factors': self.risk_factors,
            'notes': self.notes,
            'special_conditions': self.special_conditions,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'last_modified': self.last_modified.isoformat() if self.last_modified else None,
            'property_id': self.property_id,
            'client_id': self.client_id,
            'listing_agent_id': self.listing_agent_id,
            'buyer_agent_id': self.buyer_agent_id
        }
    
    def __repr__(self):
        return f'<Transaction {self.id} - {self.transaction_status}>'


class TransactionMilestone(db.Model):
    __tablename__ = 'transaction_milestones'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    
    milestone_name = db.Column(db.String(100), nullable=False)
    milestone_status = db.Column(db.String(50), default='Pending')  # Pending, In Progress, Complete, Overdue
    due_date = db.Column(db.Date)
    completed_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    
    # Automation fields
    auto_reminder_sent = db.Column(db.Boolean, default=False)
    reminder_frequency = db.Column(db.String(20))  # daily, weekly, etc.
    
    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'milestone_name': self.milestone_name,
            'milestone_status': self.milestone_status,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'notes': self.notes,
            'auto_reminder_sent': self.auto_reminder_sent,
            'reminder_frequency': self.reminder_frequency
        }


class TransactionDocument(db.Model):
    __tablename__ = 'transaction_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    
    document_name = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # Contract, Report, Financial, etc.
    document_status = db.Column(db.String(50), default='Pending')  # Pending, In Review, Complete, Signed
    file_path = db.Column(db.String(500))
    file_url = db.Column(db.String(500))
    
    uploaded_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.Date)
    signed_date = db.Column(db.Date)
    
    # Document metadata
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.String(50))
    version = db.Column(db.Integer, default=1)
    
    # Foreign keys
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    uploaded_by = db.relationship('User', backref='uploaded_documents')
    
    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'document_name': self.document_name,
            'document_type': self.document_type,
            'document_status': self.document_status,
            'file_path': self.file_path,
            'file_url': self.file_url,
            'uploaded_date': self.uploaded_date.isoformat() if self.uploaded_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'signed_date': self.signed_date.isoformat() if self.signed_date else None,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'version': self.version,
            'uploaded_by_id': self.uploaded_by_id
        }

