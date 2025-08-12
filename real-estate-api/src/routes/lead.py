from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.lead import Lead
from src.models.communication import Communication
from datetime import datetime
import json

lead_bp = Blueprint('lead', __name__)

@lead_bp.route('/leads', methods=['GET'])
def get_leads():
    """Get all leads with optional filtering"""
    try:
        # Get query parameters
        status = request.args.get('status')
        source = request.args.get('source')
        agent_id = request.args.get('agent_id')
        limit = request.args.get('limit', 50, type=int)
        
        # Build query
        query = Lead.query
        
        if status:
            query = query.filter(Lead.lead_status == status)
        if source:
            query = query.filter(Lead.lead_source == source)
        if agent_id:
            query = query.filter(Lead.assigned_agent_id == agent_id)
        
        leads = query.order_by(Lead.created_date.desc()).limit(limit).all()
        
        # Enrich with agent information
        result = []
        for lead in leads:
            lead_data = lead.to_dict()
            if lead.assigned_agent:
                lead_data['assigned_agent'] = {
                    'id': lead.assigned_agent.id,
                    'name': f"{lead.assigned_agent.first_name} {lead.assigned_agent.last_name}"
                }
            result.append(lead_data)
        
        return jsonify({
            'success': True,
            'leads': result,
            'count': len(result)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@lead_bp.route('/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Get a specific lead with communication history"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        lead_data = lead.to_dict()
        
        # Add assigned agent info
        if lead.assigned_agent:
            lead_data['assigned_agent'] = lead.assigned_agent.to_dict()
        
        # Add communication history
        communications = Communication.query.filter_by(lead_id=lead_id).order_by(Communication.sent_date.desc()).all()
        lead_data['communications'] = [comm.to_dict() for comm in communications]
        
        return jsonify({
            'success': True,
            'lead': lead_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@lead_bp.route('/leads', methods=['POST'])
def create_lead():
    """Create a new lead"""
    try:
        data = request.get_json()
        
        # Calculate initial lead score
        lead_score = calculate_lead_score(data)
        
        lead = Lead(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            lead_source=data['lead_source'],
            lead_status=data.get('lead_status', 'New'),
            lead_score=lead_score,
            property_interest=data.get('property_interest'),
            budget_min=data.get('budget_min'),
            budget_max=data.get('budget_max'),
            preferred_areas=json.dumps(data.get('preferred_areas', [])) if data.get('preferred_areas') else None,
            timeline=data.get('timeline'),
            notes=data.get('notes'),
            assigned_agent_id=data.get('assigned_agent_id')
        )
        
        db.session.add(lead)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'lead': lead.to_dict(),
            'message': 'Lead created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@lead_bp.route('/leads/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    """Update a lead"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()
        
        # Update fields
        for field in ['first_name', 'last_name', 'email', 'phone', 'lead_status', 'property_interest', 
                     'budget_min', 'budget_max', 'timeline', 'notes', 'assigned_agent_id']:
            if field in data:
                setattr(lead, field, data[field])
        
        # Handle preferred_areas as JSON
        if 'preferred_areas' in data:
            lead.preferred_areas = json.dumps(data['preferred_areas']) if data['preferred_areas'] else None
        
        # Update next follow up date
        if 'next_follow_up' in data and data['next_follow_up']:
            lead.next_follow_up = datetime.strptime(data['next_follow_up'], '%Y-%m-%d').date()
        
        # Recalculate lead score
        lead.lead_score = calculate_lead_score(data, existing_lead=lead)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'lead': lead.to_dict(),
            'message': 'Lead updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@lead_bp.route('/leads/<int:lead_id>/convert', methods=['POST'])
def convert_lead(lead_id):
    """Convert a lead to a client"""
    try:
        from src.models.client import Client
        
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()
        
        # Create client from lead
        client = Client(
            first_name=lead.first_name,
            last_name=lead.last_name,
            email=lead.email,
            phone=lead.phone,
            client_type=data.get('client_type', lead.property_interest),
            budget_min=lead.budget_min,
            budget_max=lead.budget_max,
            preferred_areas=lead.preferred_areas,
            timeline=lead.timeline,
            notes=lead.notes,
            assigned_agent_id=lead.assigned_agent_id,
            original_lead_id=lead.id,
            referral_source=lead.lead_source
        )
        
        db.session.add(client)
        
        # Update lead status
        lead.lead_status = 'Converted'
        lead.converted_client_id = client.id
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'client': client.to_dict(),
            'message': 'Lead converted to client successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@lead_bp.route('/leads/metrics', methods=['GET'])
def get_lead_metrics():
    """Get lead metrics for dashboard"""
    try:
        # Total leads
        total_leads = Lead.query.count()
        
        # New leads (last 7 days)
        from datetime import datetime, timedelta
        week_ago = datetime.now() - timedelta(days=7)
        new_leads = Lead.query.filter(Lead.created_date >= week_ago).count()
        
        # Hot leads (score >= 80)
        hot_leads = Lead.query.filter(Lead.lead_score >= 80).count()
        
        # Conversion rate
        converted_leads = Lead.query.filter(Lead.lead_status == 'Converted').count()
        conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
        
        # Leads by source
        from sqlalchemy import func
        leads_by_source = db.session.query(
            Lead.lead_source,
            func.count(Lead.id).label('count')
        ).group_by(Lead.lead_source).all()
        
        source_breakdown = {source: count for source, count in leads_by_source}
        
        # Leads by status
        leads_by_status = db.session.query(
            Lead.lead_status,
            func.count(Lead.id).label('count')
        ).group_by(Lead.lead_status).all()
        
        status_breakdown = {status: count for status, count in leads_by_status}
        
        return jsonify({
            'success': True,
            'metrics': {
                'total_leads': total_leads,
                'new_leads': new_leads,
                'hot_leads': hot_leads,
                'conversion_rate': round(conversion_rate, 1),
                'leads_by_source': source_breakdown,
                'leads_by_status': status_breakdown
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def calculate_lead_score(data, existing_lead=None):
    """Calculate lead score based on various factors"""
    score = 0
    
    # Source scoring (30 points max)
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
    
    source = data.get('lead_source') or (existing_lead.lead_source if existing_lead else 'Other')
    score += source_scores.get(source, 5)
    
    # Timeline scoring (25 points max)
    timeline_scores = {
        'ASAP': 25,
        '1-3 months': 20,
        '3-6 months': 15,
        '6-12 months': 10,
        '1+ years': 5,
        'Just browsing': 3
    }
    
    timeline = data.get('timeline') or (existing_lead.timeline if existing_lead else 'Just browsing')
    score += timeline_scores.get(timeline, 3)
    
    # Budget scoring (20 points max)
    budget_max = data.get('budget_max') or (existing_lead.budget_max if existing_lead else 0)
    if budget_max:
        if budget_max >= 1000000:
            score += 20
        elif budget_max >= 500000:
            score += 15
        elif budget_max >= 300000:
            score += 10
        elif budget_max >= 200000:
            score += 8
        else:
            score += 5
    
    # Property interest scoring (15 points max)
    interest_scores = {
        'Buying': 15,
        'Both': 12,
        'Selling': 10,
        'Investing': 8,
        'Renting': 3
    }
    
    interest = data.get('property_interest') or (existing_lead.property_interest if existing_lead else 'Buying')
    score += interest_scores.get(interest, 5)
    
    # Contact completeness (10 points max)
    if data.get('email') or (existing_lead and existing_lead.email):
        score += 5
    if data.get('phone') or (existing_lead and existing_lead.phone):
        score += 5
    
    return min(score, 100)  # Cap at 100

