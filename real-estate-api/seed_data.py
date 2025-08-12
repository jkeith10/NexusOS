#!/usr/bin/env python3
"""
Seed script to populate the real estate CRM database with sample data
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, date, timedelta
from src.models.user import db, User
from src.models.lead import Lead
from src.models.client import Client
from src.models.property import Property
from src.models.transaction import Transaction, TransactionMilestone, TransactionDocument
from src.models.communication import Communication
from src.models.marketing_campaign import MarketingCampaign
from src.main import app
import json

def seed_database():
    """Seed the database with sample data"""
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create sample users (agents)
        print("Creating sample agents...")
        agents = [
            User(
                first_name="Sarah",
                last_name="Johnson",
                email="sarah.johnson@realty.com",
                phone="(555) 123-4567",
                role="Agent",
                license_number="RE123456",
                license_state="CA",
                commission_rate=0.03,
                ytd_transactions=15,
                ytd_volume=4250000,
                ytd_commission=127500,
                territory=json.dumps(["Downtown", "Waterfront"]),
                brokerage_name="Premier Realty Group"
            ),
            User(
                first_name="Mike",
                last_name="Rodriguez",
                email="mike.rodriguez@realty.com",
                phone="(555) 234-5678",
                role="Agent",
                license_number="RE234567",
                license_state="CA",
                commission_rate=0.03,
                ytd_transactions=12,
                ytd_volume=3100000,
                ytd_commission=93000,
                territory=json.dumps(["Suburbs", "Historic District"]),
                brokerage_name="Premier Realty Group"
            ),
            User(
                first_name="Jennifer",
                last_name="Lee",
                email="jennifer.lee@realty.com",
                phone="(555) 345-6789",
                role="Agent",
                license_number="RE345678",
                license_state="CA",
                commission_rate=0.03,
                ytd_transactions=18,
                ytd_volume=5200000,
                ytd_commission=156000,
                territory=json.dumps(["New Development", "Rural"]),
                brokerage_name="Premier Realty Group"
            )
        ]
        
        for agent in agents:
            db.session.add(agent)
        
        db.session.commit()
        
        # Create sample leads
        print("Creating sample leads...")
        leads = [
            Lead(
                first_name="John",
                last_name="Smith",
                email="john.smith@email.com",
                phone="(555) 111-2222",
                lead_source="Website Form",
                lead_status="Qualified",
                lead_score=85,
                property_interest="Buying",
                budget_min=400000,
                budget_max=600000,
                preferred_areas=json.dumps(["Downtown", "Waterfront"]),
                timeline="1-3 months",
                notes="Looking for a 3BR condo with water views",
                assigned_agent_id=1,
                created_date=datetime.now() - timedelta(days=5)
            ),
            Lead(
                first_name="Emily",
                last_name="Davis",
                email="emily.davis@email.com",
                phone="(555) 222-3333",
                lead_source="Referral",
                lead_status="New",
                lead_score=92,
                property_interest="Selling",
                budget_min=500000,
                budget_max=700000,
                preferred_areas=json.dumps(["Suburbs"]),
                timeline="ASAP",
                notes="Inherited property, needs quick sale",
                assigned_agent_id=2,
                created_date=datetime.now() - timedelta(days=2)
            ),
            Lead(
                first_name="Robert",
                last_name="Wilson",
                email="robert.wilson@email.com",
                phone="(555) 333-4444",
                lead_source="Google Ads",
                lead_status="Nurturing",
                lead_score=65,
                property_interest="Both",
                budget_min=300000,
                budget_max=500000,
                preferred_areas=json.dumps(["Historic District", "Downtown"]),
                timeline="6-12 months",
                notes="First-time buyer, needs education",
                assigned_agent_id=3,
                created_date=datetime.now() - timedelta(days=10)
            )
        ]
        
        for lead in leads:
            db.session.add(lead)
        
        db.session.commit()
        
        # Create sample clients
        print("Creating sample clients...")
        clients = [
            Client(
                first_name="Michael",
                last_name="Brown",
                email="michael.brown@email.com",
                phone="(555) 444-5555",
                client_type="Buyer",
                budget_min=450000,
                budget_max=650000,
                preferred_areas=json.dumps(["Downtown", "Waterfront"]),
                timeline="1-3 months",
                pre_approved=True,
                pre_approval_amount=600000,
                assigned_agent_id=1,
                created_date=datetime.now() - timedelta(days=30)
            ),
            Client(
                first_name="Lisa",
                last_name="Anderson",
                email="lisa.anderson@email.com",
                phone="(555) 555-6666",
                client_type="Seller",
                assigned_agent_id=2,
                created_date=datetime.now() - timedelta(days=45)
            ),
            Client(
                first_name="David",
                last_name="Taylor",
                email="david.taylor@email.com",
                phone="(555) 666-7777",
                client_type="Buyer",
                budget_min=600000,
                budget_max=800000,
                preferred_areas=json.dumps(["New Development"]),
                timeline="ASAP",
                pre_approved=True,
                pre_approval_amount=750000,
                assigned_agent_id=3,
                created_date=datetime.now() - timedelta(days=20)
            )
        ]
        
        for client in clients:
            db.session.add(client)
        
        db.session.commit()
        
        # Create sample properties
        print("Creating sample properties...")
        properties = [
            Property(
                address="123 Main Street",
                city="Anytown",
                state="CA",
                zip_code="12345",
                property_type="Single Family",
                bedrooms=3,
                bathrooms=2.5,
                square_feet=2200,
                listing_price=450000,
                listing_status="Under Contract",
                listing_date=date.today() - timedelta(days=30),
                days_on_market=30,
                mls_number="MLS123456",
                listing_agent_id=1
            ),
            Property(
                address="456 Oak Avenue",
                city="Anytown",
                state="CA",
                zip_code="12346",
                property_type="Condo",
                bedrooms=2,
                bathrooms=2,
                square_feet=1400,
                listing_price=325000,
                listing_status="Active",
                listing_date=date.today() - timedelta(days=15),
                days_on_market=15,
                mls_number="MLS234567",
                listing_agent_id=2
            ),
            Property(
                address="789 Pine Road",
                city="Anytown",
                state="CA",
                zip_code="12347",
                property_type="Single Family",
                bedrooms=4,
                bathrooms=3,
                square_feet=2800,
                listing_price=650000,
                listing_status="Pending",
                listing_date=date.today() - timedelta(days=45),
                days_on_market=45,
                mls_number="MLS345678",
                listing_agent_id=3
            )
        ]
        
        for property in properties:
            db.session.add(property)
        
        db.session.commit()
        
        # Create sample transactions
        print("Creating sample transactions...")
        transactions = [
            Transaction(
                transaction_type="Purchase",
                transaction_status="Under Contract",
                property_id=1,
                client_id=1,
                listing_agent_id=1,
                buyer_agent_id=1,
                contract_date=date.today() - timedelta(days=25),
                closing_date=date.today() + timedelta(days=5),
                sale_price=450000,
                commission_rate=0.06,
                total_commission=27000,
                listing_commission=13500,
                buyer_commission=13500,
                progress_percentage=65,
                risk_level="Low",
                risk_score=25
            ),
            Transaction(
                transaction_type="Purchase",
                transaction_status="Inspection Period",
                property_id=2,
                client_id=2,
                listing_agent_id=2,
                buyer_agent_id=2,
                contract_date=date.today() - timedelta(days=10),
                closing_date=date.today() + timedelta(days=20),
                sale_price=325000,
                commission_rate=0.06,
                total_commission=19500,
                listing_commission=9750,
                buyer_commission=9750,
                progress_percentage=35,
                risk_level="Medium",
                risk_score=45
            ),
            Transaction(
                transaction_type="Purchase",
                transaction_status="Clear to Close",
                property_id=3,
                client_id=3,
                listing_agent_id=3,
                buyer_agent_id=3,
                contract_date=date.today() - timedelta(days=35),
                closing_date=date.today() + timedelta(days=3),
                sale_price=650000,
                commission_rate=0.06,
                total_commission=39000,
                listing_commission=19500,
                buyer_commission=19500,
                progress_percentage=90,
                risk_level="Low",
                risk_score=15
            )
        ]
        
        for transaction in transactions:
            db.session.add(transaction)
        
        db.session.commit()
        
        # Create sample milestones for each transaction
        print("Creating sample transaction milestones...")
        milestone_templates = [
            {"name": "Contract Signed", "status": "Complete"},
            {"name": "Inspection Scheduled", "status": "Complete"},
            {"name": "Inspection Complete", "status": "Complete"},
            {"name": "Appraisal Ordered", "status": "Complete"},
            {"name": "Appraisal Complete", "status": "In Progress"},
            {"name": "Final Walkthrough", "status": "Pending"},
            {"name": "Closing", "status": "Pending"}
        ]
        
        for i, transaction in enumerate(transactions, 1):
            for j, milestone_template in enumerate(milestone_templates):
                # Adjust status based on transaction progress
                if transaction.progress_percentage >= (j + 1) * 14:  # Roughly 14% per milestone
                    status = "Complete"
                elif transaction.progress_percentage >= j * 14:
                    status = "In Progress"
                else:
                    status = "Pending"
                
                milestone = TransactionMilestone(
                    transaction_id=i,
                    milestone_name=milestone_template["name"],
                    milestone_status=status,
                    due_date=transaction.contract_date + timedelta(days=j * 5) if transaction.contract_date else None,
                    completed_date=transaction.contract_date + timedelta(days=j * 4) if status == "Complete" and transaction.contract_date else None
                )
                db.session.add(milestone)
        
        # Create sample documents
        print("Creating sample transaction documents...")
        document_templates = [
            {"name": "Purchase Agreement", "type": "Contract", "status": "Signed"},
            {"name": "Inspection Report", "type": "Report", "status": "Complete"},
            {"name": "Appraisal Report", "type": "Report", "status": "Pending"},
            {"name": "Loan Documents", "type": "Financial", "status": "In Review"}
        ]
        
        for i, transaction in enumerate(transactions, 1):
            for doc_template in document_templates:
                document = TransactionDocument(
                    transaction_id=i,
                    document_name=doc_template["name"],
                    document_type=doc_template["type"],
                    document_status=doc_template["status"],
                    uploaded_date=datetime.now() - timedelta(days=20),
                    uploaded_by_id=transaction.listing_agent_id
                )
                db.session.add(document)
        
        # Create sample marketing campaigns
        print("Creating sample marketing campaigns...")
        campaigns = [
            MarketingCampaign(
                campaign_name="Downtown Luxury Listings",
                campaign_type="Email",
                campaign_status="Active",
                description="Showcase premium downtown properties",
                target_audience="Luxury Buyers",
                budget=2500,
                start_date=date.today() - timedelta(days=30),
                end_date=date.today() + timedelta(days=30),
                emails_sent=1250,
                emails_delivered=1200,
                emails_opened=480,
                emails_clicked=96,
                leads_generated=12,
                cost_per_lead=208.33,
                roi=2.4,
                created_by_id=1,
                property_id=1
            ),
            MarketingCampaign(
                campaign_name="First-Time Buyer Workshop",
                campaign_type="Social",
                campaign_status="Completed",
                description="Educational content for new buyers",
                target_audience="First-Time Buyers",
                budget=1500,
                start_date=date.today() - timedelta(days=60),
                end_date=date.today() - timedelta(days=30),
                social_posts=25,
                social_engagement=340,
                social_shares=45,
                leads_generated=8,
                cost_per_lead=187.50,
                roi=1.8,
                created_by_id=2
            )
        ]
        
        for campaign in campaigns:
            db.session.add(campaign)
        
        # Create sample communications
        print("Creating sample communications...")
        communications = [
            Communication(
                communication_type="Email",
                direction="Outbound",
                subject="Welcome to Premier Realty",
                content="Thank you for your interest in our services...",
                status="Delivered",
                user_id=1,
                lead_id=1,
                sent_date=datetime.now() - timedelta(days=5),
                delivered_date=datetime.now() - timedelta(days=5),
                opened=True,
                is_automated=True,
                automation_trigger="New Lead"
            ),
            Communication(
                communication_type="SMS",
                direction="Outbound",
                content="Hi Emily, thanks for the referral! I'll call you tomorrow to discuss your property sale.",
                status="Delivered",
                user_id=2,
                lead_id=2,
                sent_date=datetime.now() - timedelta(days=2),
                delivered_date=datetime.now() - timedelta(days=2),
                cost=0.05
            ),
            Communication(
                communication_type="Call",
                direction="Outbound",
                subject="Property Consultation",
                content="Discussed client's needs and scheduled property viewing",
                status="Completed",
                user_id=1,
                client_id=1,
                sent_date=datetime.now() - timedelta(days=1)
            )
        ]
        
        for comm in communications:
            db.session.add(comm)
        
        db.session.commit()
        
        print("✅ Database seeded successfully!")
        print(f"Created:")
        print(f"  - {len(agents)} agents")
        print(f"  - {len(leads)} leads")
        print(f"  - {len(clients)} clients")
        print(f"  - {len(properties)} properties")
        print(f"  - {len(transactions)} transactions")
        print(f"  - {len(milestone_templates) * len(transactions)} milestones")
        print(f"  - {len(document_templates) * len(transactions)} documents")
        print(f"  - {len(campaigns)} marketing campaigns")
        print(f"  - {len(communications)} communications")

if __name__ == "__main__":
    seed_database()

