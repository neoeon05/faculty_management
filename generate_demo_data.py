"""
Demo Data Generator for Faculty Management System

This script generates sample data for testing the application.
Run this script to populate the system with demo faculties and sessions.

Usage:
    python generate_demo_data.py
"""

import json
from datetime import datetime, timedelta
import random
from pathlib import Path

# Create data directory
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Sample data
SAMPLE_FACULTIES = [
    {
        "name": "Dr. Sarah Johnson",
        "gender": "Female",
        "email": "sarah.johnson@university.edu",
        "designation": "Professor",
        "batch": "MBA 2024",
        "biodata": "PhD in Computer Science from MIT. 15 years of teaching experience in Data Science and Machine Learning. Published over 30 research papers."
    },
    {
        "name": "Prof. Michael Chen",
        "gender": "Male",
        "email": "michael.chen@university.edu",
        "designation": "Professor",
        "batch": "MBA 2024",
        "biodata": "Expert in Financial Management with 20 years of industry experience. Former CFO of Fortune 500 company."
    },
    {
        "name": "Dr. Priya Sharma",
        "gender": "Female",
        "email": "priya.sharma@university.edu",
        "designation": "Associate Professor",
        "batch": "MBA 2023",
        "biodata": "Specializes in Marketing and Consumer Behavior. Worked with leading FMCG companies for 12 years."
    },
    {
        "name": "Prof. Robert Williams",
        "gender": "Male",
        "email": "robert.williams@university.edu",
        "designation": "Professor",
        "batch": "MBA 2024",
        "biodata": "Operations Management expert. Certified Six Sigma Black Belt. 18 years in manufacturing and logistics."
    },
    {
        "name": "Dr. Anita Desai",
        "gender": "Female",
        "email": "anita.desai@university.edu",
        "designation": "Assistant Professor",
        "batch": "MBA 2023",
        "biodata": "Human Resource Management specialist. SHRM certified. 14 years of experience in organizational development."
    },
    {
        "name": "Prof. David Kumar",
        "gender": "Male",
        "email": "david.kumar@university.edu",
        "designation": "Professor",
        "batch": "MBA 2024",
        "biodata": "Strategic Management and Business Policy expert. Former consultant at McKinsey & Company for 10 years."
    },
    {
        "name": "Dr. Emily White",
        "gender": "Female",
        "email": "emily.white@university.edu",
        "designation": "Associate Professor",
        "batch": "MBA 2023",
        "biodata": "Economics and Business Analytics specialist. Published author of 3 books on econometrics."
    },
    {
        "name": "Prof. Rajesh Patel",
        "gender": "Male",
        "email": "rajesh.patel@university.edu",
        "designation": "Adjunct Professor",
        "batch": "MBA 2024",
        "biodata": "Entrepreneurship and Innovation expert. Founded 3 successful startups. Angel investor."
    }
]

SAMPLE_SESSIONS = [
    {
        "name": "Introduction to Data Science",
        "duration": 2.0,
        "batch": "MBA 2024 Section A"
    },
    {
        "name": "Financial Statement Analysis",
        "duration": 3.0,
        "batch": "MBA 2024 Section B"
    },
    {
        "name": "Digital Marketing Strategies",
        "duration": 2.5,
        "batch": "MBA 2023 Section A"
    },
    {
        "name": "Supply Chain Optimization",
        "duration": 2.0,
        "batch": "MBA 2024 Section A"
    },
    {
        "name": "Talent Management & Retention",
        "duration": 1.5,
        "batch": "MBA 2023 Section B"
    },
    {
        "name": "Corporate Strategy",
        "duration": 3.0,
        "batch": "MBA 2024 Section B"
    },
    {
        "name": "Business Forecasting",
        "duration": 2.0,
        "batch": "MBA 2023 Section A"
    },
    {
        "name": "Startup Ecosystem & Funding",
        "duration": 2.5,
        "batch": "MBA 2024 Section A"
    },
    {
        "name": "Machine Learning Applications",
        "duration": 3.0,
        "batch": "MBA 2024 Section B"
    },
    {
        "name": "Investment Banking Fundamentals",
        "duration": 2.5,
        "batch": "MBA 2023 Section B"
    },
    {
        "name": "Consumer Psychology",
        "duration": 2.0,
        "batch": "MBA 2024 Section A"
    },
    {
        "name": "Lean Six Sigma Principles",
        "duration": 3.0,
        "batch": "MBA 2023 Section A"
    },
    {
        "name": "Performance Management Systems",
        "duration": 2.0,
        "batch": "MBA 2024 Section B"
    },
    {
        "name": "Business Model Innovation",
        "duration": 2.5,
        "batch": "MBA 2023 Section B"
    },
    {
        "name": "Predictive Analytics",
        "duration": 3.0,
        "batch": "MBA 2024 Section A"
    }
]

def generate_feedback():
    """Generate random feedback scores based on max marks for each field"""
    return {
        "relevance": round(random.uniform(2.5, 4.0), 2),  # Max 4
        "knowledge": round(random.uniform(3.5, 5.0), 2),  # Max 5
        "practical_linking": round(random.uniform(3.0, 5.0), 2),  # Max 5
        "coverage": round(random.uniform(3.5, 5.0), 2),  # Max 5
        "presentation_style": round(random.uniform(3.5, 5.0), 2),  # Max 5
        "audibility": round(random.uniform(3.5, 5.0), 2),  # Max 5
        "interaction": round(random.uniform(3.0, 5.0), 2),  # Max 5
        "response": round(random.uniform(3.5, 5.0), 2),  # Max 5
        "teaching_aids": round(random.uniform(3.0, 5.0), 2),  # Max 5
        "pace": round(random.uniform(2.0, 3.0), 2),  # Max 3
        "overall_performance": round(random.uniform(3.5, 5.0), 2),  # Max 5
        "recommend_again": random.choice([
            "Yes, highly recommended. Excellent teaching skills.",
            "Yes, would definitely recommend for future sessions.",
            "Yes, very knowledgeable and engaging instructor.",
            "Absolutely! One of the best sessions we've had.",
            "Yes, recommend with minor improvements in time management."
        ])
    }

def generate_demo_data():
    """Generate demo faculties and sessions"""
    
    print("🎓 Generating demo data for Faculty Management System...")
    print()
    
    # Generate faculties
    faculties = {}
    print("👥 Creating sample faculties...")
    for i, faculty_data in enumerate(SAMPLE_FACULTIES, 1):
        faculty_id = f"FAC{i:04d}"
        faculties[faculty_id] = {
            "id": faculty_id,
            **faculty_data,
            "created_by": "demo",
            "created_at": datetime.now().isoformat()
        }
        print(f"   ✓ Created: {faculty_data['name']}")
    
    # Save faculties
    faculties_file = DATA_DIR / "faculties.json"
    with open(faculties_file, 'w') as f:
        json.dump(faculties, f, indent=2)
    print(f"\n✅ Saved {len(faculties)} faculties to {faculties_file}")
    
    # Generate sessions
    sessions = {}
    print("\n📚 Creating sample sessions...")
    
    faculty_names = [f["name"] for f in faculties.values()]
    start_date = datetime.now() - timedelta(days=90)  # Last 3 months
    
    for i, session_data in enumerate(SAMPLE_SESSIONS, 1):
        session_id = f"SES{i:04d}"
        
        # Random date in the last 90 days
        random_days = random.randint(0, 89)
        session_date = start_date + timedelta(days=random_days)
        
        # Random faculty
        faculty_name = random.choice(faculty_names)
        
        # Random honorarium based on duration
        base_honorarium = session_data["duration"] * 2000
        honorarium = base_honorarium + random.randint(-500, 1000)
        
        sessions[session_id] = {
            "id": session_id,
            "date": session_date.strftime("%Y-%m-%d"),
            "faculty_name": faculty_name,
            "session_name": session_data["name"],
            "duration": session_data["duration"],
            "batch": session_data["batch"],
            "honorarium_paid": honorarium,
            "feedback": generate_feedback(),
            "created_by": "demo",
            "created_at": datetime.now().isoformat()
        }
        print(f"   ✓ Created: {session_data['name']} by {faculty_name}")
    
    # Save sessions
    sessions_file = DATA_DIR / "sessions.json"
    with open(sessions_file, 'w') as f:
        json.dump(sessions, f, indent=2)
    print(f"\n✅ Saved {len(sessions)} sessions to {sessions_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 DEMO DATA SUMMARY")
    print("="*60)
    print(f"Total Faculties: {len(faculties)}")
    print(f"Total Sessions: {len(sessions)}")
    print(f"Total Honorarium: ₹{sum(s['honorarium_paid'] for s in sessions.values()):,.2f}")
    print(f"Date Range: {min(s['date'] for s in sessions.values())} to {max(s['date'] for s in sessions.values())}")
    
    # Calculate average feedback
    all_scores = []
    for session in sessions.values():
        feedback = session['feedback']
        scores = [v for k, v in feedback.items() if k != 'recommend_again']
        all_scores.extend(scores)
    avg_feedback = sum(all_scores) / len(all_scores)
    print(f"Average Feedback Score: {avg_feedback:.2f}/10")
    print("="*60)
    print()
    print("🎉 Demo data generated successfully!")
    print()
    print("📝 Next steps:")
    print("   1. Run: streamlit run app.py")
    print("   2. Login with: admin / admin123")
    print("   3. Explore the demo data!")
    print()

if __name__ == "__main__":
    try:
        generate_demo_data()
    except Exception as e:
        print(f"\n❌ Error generating demo data: {str(e)}")
        print("Please ensure you're running this script from the project root directory.")
