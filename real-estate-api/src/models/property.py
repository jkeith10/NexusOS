from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Property(db.Model):
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Address information
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    county = db.Column(db.String(100))
    
    # Property details
    property_type = db.Column(db.String(50), nullable=False)  # Single Family, Condo, etc.
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Float)
    square_feet = db.Column(db.Integer)
    lot_size = db.Column(db.Float)
    year_built = db.Column(db.Integer)
    garage_spaces = db.Column(db.Integer)
    
    # Listing information
    listing_price = db.Column(db.Float)
    listing_status = db.Column(db.String(50), default='Active')  # Active, Pending, Sold, Withdrawn
    listing_date = db.Column(db.Date)
    days_on_market = db.Column(db.Integer)
    
    # MLS and external data
    mls_number = db.Column(db.String(50), unique=True)
    mls_status = db.Column(db.String(50))
    mls_last_updated = db.Column(db.DateTime)
    
    # Property features
    features = db.Column(db.Text)  # JSON string of features
    description = db.Column(db.Text)
    private_remarks = db.Column(db.Text)
    
    # Financial information
    property_taxes = db.Column(db.Float)
    hoa_fees = db.Column(db.Float)
    estimated_monthly_payment = db.Column(db.Float)
    
    # Marketing information
    marketing_status = db.Column(db.String(50), default='Not Started')
    photos_count = db.Column(db.Integer, default=0)
    virtual_tour_url = db.Column(db.String(500))
    listing_url = db.Column(db.String(500))
    
    # Timestamps
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    listing_agent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    seller_client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    
    # Relationships
    listing_agent = db.relationship('User', backref='listed_properties')
    seller_client = db.relationship('Client', backref='properties_for_sale')
    transactions = db.relationship('Transaction', backref='property')
    marketing_campaigns = db.relationship('MarketingCampaign', backref='featured_property')
    
    def to_dict(self):
        return {
            'id': self.id,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'county': self.county,
            'property_type': self.property_type,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'square_feet': self.square_feet,
            'lot_size': self.lot_size,
            'year_built': self.year_built,
            'garage_spaces': self.garage_spaces,
            'listing_price': self.listing_price,
            'listing_status': self.listing_status,
            'listing_date': self.listing_date.isoformat() if self.listing_date else None,
            'days_on_market': self.days_on_market,
            'mls_number': self.mls_number,
            'mls_status': self.mls_status,
            'mls_last_updated': self.mls_last_updated.isoformat() if self.mls_last_updated else None,
            'features': self.features,
            'description': self.description,
            'private_remarks': self.private_remarks,
            'property_taxes': self.property_taxes,
            'hoa_fees': self.hoa_fees,
            'estimated_monthly_payment': self.estimated_monthly_payment,
            'marketing_status': self.marketing_status,
            'photos_count': self.photos_count,
            'virtual_tour_url': self.virtual_tour_url,
            'listing_url': self.listing_url,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'last_modified': self.last_modified.isoformat() if self.last_modified else None,
            'listing_agent_id': self.listing_agent_id,
            'seller_client_id': self.seller_client_id
        }
    
    def __repr__(self):
        return f'<Property {self.address}, {self.city}>'

