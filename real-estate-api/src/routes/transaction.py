from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.transaction import Transaction, TransactionMilestone, TransactionDocument
from src.models.property import Property
from src.models.client import Client
from datetime import datetime, date
import json

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions with optional filtering"""
    try:
        # Get query parameters
        status = request.args.get('status')
        agent_id = request.args.get('agent_id')
        limit = request.args.get('limit', 50, type=int)
        
        # Build query
        query = Transaction.query
        
        if status:
            query = query.filter(Transaction.transaction_status == status)
        if agent_id:
            query = query.filter(
                (Transaction.listing_agent_id == agent_id) | 
                (Transaction.buyer_agent_id == agent_id)
            )
        
        transactions = query.limit(limit).all()
        
        # Enrich with related data
        result = []
        for transaction in transactions:
            transaction_data = transaction.to_dict()
            
            # Add property information
            if transaction.property:
                transaction_data['property'] = transaction.property.to_dict()
            
            # Add client information
            if transaction.client:
                transaction_data['client'] = transaction.client.to_dict()
            
            # Add agent information
            if transaction.listing_agent:
                transaction_data['listing_agent'] = {
                    'id': transaction.listing_agent.id,
                    'name': f"{transaction.listing_agent.first_name} {transaction.listing_agent.last_name}"
                }
            
            if transaction.buyer_agent:
                transaction_data['buyer_agent'] = {
                    'id': transaction.buyer_agent.id,
                    'name': f"{transaction.buyer_agent.first_name} {transaction.buyer_agent.last_name}"
                }
            
            # Add milestones
            milestones = TransactionMilestone.query.filter_by(transaction_id=transaction.id).all()
            transaction_data['milestones'] = [milestone.to_dict() for milestone in milestones]
            
            # Add documents
            documents = TransactionDocument.query.filter_by(transaction_id=transaction.id).all()
            transaction_data['documents'] = [doc.to_dict() for doc in documents]
            
            result.append(transaction_data)
        
        return jsonify({
            'success': True,
            'transactions': result,
            'count': len(result)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    """Get a specific transaction with all related data"""
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        transaction_data = transaction.to_dict()
        
        # Add property information
        if transaction.property:
            transaction_data['property'] = transaction.property.to_dict()
        
        # Add client information
        if transaction.client:
            transaction_data['client'] = transaction.client.to_dict()
        
        # Add agent information
        if transaction.listing_agent:
            transaction_data['listing_agent'] = transaction.listing_agent.to_dict()
        
        if transaction.buyer_agent:
            transaction_data['buyer_agent'] = transaction.buyer_agent.to_dict()
        
        # Add milestones
        milestones = TransactionMilestone.query.filter_by(transaction_id=transaction.id).all()
        transaction_data['milestones'] = [milestone.to_dict() for milestone in milestones]
        
        # Add documents
        documents = TransactionDocument.query.filter_by(transaction_id=transaction.id).all()
        transaction_data['documents'] = [doc.to_dict() for doc in documents]
        
        return jsonify({
            'success': True,
            'transaction': transaction_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction"""
    try:
        data = request.get_json()
        
        # Create transaction
        transaction = Transaction(
            transaction_type=data.get('transaction_type', 'Purchase'),
            transaction_status=data.get('transaction_status', 'Active'),
            property_id=data['property_id'],
            client_id=data['client_id'],
            listing_agent_id=data.get('listing_agent_id'),
            buyer_agent_id=data.get('buyer_agent_id'),
            contract_date=datetime.strptime(data['contract_date'], '%Y-%m-%d').date() if data.get('contract_date') else None,
            closing_date=datetime.strptime(data['closing_date'], '%Y-%m-%d').date() if data.get('closing_date') else None,
            sale_price=data.get('sale_price'),
            commission_rate=data.get('commission_rate', 0.06),
            notes=data.get('notes')
        )
        
        # Calculate commission
        if transaction.sale_price and transaction.commission_rate:
            transaction.total_commission = transaction.sale_price * transaction.commission_rate
            transaction.listing_commission = transaction.total_commission / 2
            transaction.buyer_commission = transaction.total_commission / 2
        
        db.session.add(transaction)
        db.session.flush()  # Get the ID
        
        # Create default milestones
        default_milestones = [
            {'name': 'Contract Signed', 'status': 'Complete', 'due_date': transaction.contract_date},
            {'name': 'Inspection Scheduled', 'status': 'Pending', 'due_date': None},
            {'name': 'Inspection Complete', 'status': 'Pending', 'due_date': None},
            {'name': 'Appraisal Ordered', 'status': 'Pending', 'due_date': None},
            {'name': 'Appraisal Complete', 'status': 'Pending', 'due_date': None},
            {'name': 'Final Walkthrough', 'status': 'Pending', 'due_date': None},
            {'name': 'Closing', 'status': 'Pending', 'due_date': transaction.closing_date}
        ]
        
        for milestone_data in default_milestones:
            milestone = TransactionMilestone(
                transaction_id=transaction.id,
                milestone_name=milestone_data['name'],
                milestone_status=milestone_data['status'],
                due_date=milestone_data['due_date']
            )
            db.session.add(milestone)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'transaction': transaction.to_dict(),
            'message': 'Transaction created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    """Update a transaction"""
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        data = request.get_json()
        
        # Update fields
        for field in ['transaction_status', 'sale_price', 'commission_rate', 'notes', 'risk_level', 'progress_percentage']:
            if field in data:
                setattr(transaction, field, data[field])
        
        # Update dates
        for date_field in ['contract_date', 'closing_date', 'inspection_date', 'appraisal_date']:
            if date_field in data and data[date_field]:
                setattr(transaction, date_field, datetime.strptime(data[date_field], '%Y-%m-%d').date())
        
        # Recalculate commission if needed
        if 'sale_price' in data or 'commission_rate' in data:
            if transaction.sale_price and transaction.commission_rate:
                transaction.total_commission = transaction.sale_price * transaction.commission_rate
                transaction.listing_commission = transaction.total_commission / 2
                transaction.buyer_commission = transaction.total_commission / 2
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'transaction': transaction.to_dict(),
            'message': 'Transaction updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@transaction_bp.route('/transactions/<int:transaction_id>/milestones', methods=['POST'])
def update_milestone(transaction_id):
    """Update a transaction milestone"""
    try:
        data = request.get_json()
        milestone_id = data.get('milestone_id')
        
        milestone = TransactionMilestone.query.filter_by(
            id=milestone_id,
            transaction_id=transaction_id
        ).first_or_404()
        
        # Update milestone
        if 'milestone_status' in data:
            milestone.milestone_status = data['milestone_status']
        
        if 'completed_date' in data and data['completed_date']:
            milestone.completed_date = datetime.strptime(data['completed_date'], '%Y-%m-%d').date()
        
        if 'notes' in data:
            milestone.notes = data['notes']
        
        # Update transaction progress
        transaction = Transaction.query.get(transaction_id)
        completed_milestones = TransactionMilestone.query.filter_by(
            transaction_id=transaction_id,
            milestone_status='Complete'
        ).count()
        
        total_milestones = TransactionMilestone.query.filter_by(transaction_id=transaction_id).count()
        
        if total_milestones > 0:
            transaction.progress_percentage = int((completed_milestones / total_milestones) * 100)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'milestone': milestone.to_dict(),
            'message': 'Milestone updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@transaction_bp.route('/transactions/metrics', methods=['GET'])
def get_transaction_metrics():
    """Get transaction metrics for dashboard"""
    try:
        # Get basic counts
        total_active = Transaction.query.filter(Transaction.transaction_status.in_(['Active', 'Under Contract', 'Pending'])).count()
        
        # Closing this week
        from datetime import datetime, timedelta
        today = datetime.now().date()
        week_end = today + timedelta(days=7)
        
        closing_this_week = Transaction.query.filter(
            Transaction.closing_date.between(today, week_end),
            Transaction.transaction_status != 'Closed'
        ).count()
        
        # At risk transactions (high risk level or overdue milestones)
        at_risk = Transaction.query.filter(Transaction.risk_level == 'High').count()
        
        # Total volume
        total_volume = db.session.query(db.func.sum(Transaction.sale_price)).filter(
            Transaction.transaction_status == 'Closed'
        ).scalar() or 0
        
        # Average days to close
        closed_transactions = Transaction.query.filter(
            Transaction.transaction_status == 'Closed',
            Transaction.contract_date.isnot(None),
            Transaction.actual_closing_date.isnot(None)
        ).all()
        
        if closed_transactions:
            total_days = sum([
                (t.actual_closing_date - t.contract_date).days 
                for t in closed_transactions
            ])
            avg_days_to_close = total_days / len(closed_transactions)
        else:
            avg_days_to_close = 0
        
        # Success rate
        total_transactions = Transaction.query.count()
        successful_transactions = Transaction.query.filter(Transaction.transaction_status == 'Closed').count()
        success_rate = (successful_transactions / total_transactions * 100) if total_transactions > 0 else 0
        
        return jsonify({
            'success': True,
            'metrics': {
                'total_active': total_active,
                'closing_this_week': closing_this_week,
                'at_risk': at_risk,
                'total_volume': total_volume,
                'avg_days_to_close': round(avg_days_to_close),
                'success_rate': round(success_rate)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

