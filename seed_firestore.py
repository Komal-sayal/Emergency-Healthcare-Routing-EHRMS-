"""
database/firebase/seed_firestore.py
────────────────────────────────────────────────────────────────────────────
Populates Firestore with the initial hospital and ambulance data.
Run ONCE after setting up Firebase.

Usage:
    cd EHVRM-System/backend
    python ../database/firebase/seed_firestore.py

Requirements:
    pip install firebase-admin python-dotenv
    Make sure serviceAccountKey.json is in database/firebase/
────────────────────────────────────────────────────────────────────────────
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '../../backend/.env'))

import firebase_admin
from firebase_admin import credentials, firestore

# ── Init ─────────────────────────────────────────────────────────────────────
cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
if not os.path.exists(cred_path):
    print("❌  serviceAccountKey.json not found at:", cred_path)
    print("   Download it from Firebase Console → Project Settings → Service accounts")
    sys.exit(1)

if not firebase_admin._apps:
    firebase_admin.initialize_app(credentials.Certificate(cred_path))

db = firestore.client()

# ── Import data ───────────────────────────────────────────────────────────────
from models.hospital_data import HOSPITALS, AMBULANCES

def seed_hospitals():
    print("\n📥  Seeding hospitals...")
    col = db.collection('hospitals')
    for h in HOSPITALS:
        doc_id = str(h['id'])
        col.document(doc_id).set({
            'id':               h['id'],
            'name':             h['name'],
            'address':          h['address'],
            'lat':              h['lat'],
            'lng':              h['lng'],
            'phone':            h['phone'],
            'type':             h['type'],
            'established':      h['established'],
            'accreditation':    h['accreditation'],
            'website':          h.get('website', ''),
            'total_beds':       h['total_beds'],
            'available_beds':   h['available_beds'],
            'icu_total':        h['icu_total'],
            'icu_available':    h['icu_available'],
            'trauma_total':     h['trauma_total'],
            'trauma_available': h['trauma_available'],
            'burn_total':       h['burn_total'],
            'burn_available':   h['burn_available'],
            'equipment':        h['equipment'],
            'specialists':      h['specialists'],
            'rating':           h['rating'],
            'status':           h['status'],
            'ambulances':       h['ambulances'],
            'er_wait_min':      h['er_wait_min'],
            'budget_tier':      h['budget_tier'],
            'consultation_fee': h.get('consultation_fee'),
            'emergency_fee':    h.get('emergency_fee'),
            'icu_per_day':      h.get('icu_per_day'),
            'surgery_range':    h.get('surgery_range'),
            'about':            h.get('about', ''),
            'key_doctors':      h.get('key_doctors', []),
            'services':         h.get('services', []),
            'last_updated':     firestore.SERVER_TIMESTAMP,
        })
        print(f"   ✓ {h['name']}")
    print(f"   Seeded {len(HOSPITALS)} hospitals.")


def seed_ambulances():
    print("\n🚑  Seeding ambulances...")
    col = db.collection('ambulances')
    for a in AMBULANCES:
        col.document(a['id']).set({
            **a,
            'ts': firestore.SERVER_TIMESTAMP,
        })
        print(f"   ✓ {a['id']} — {a['driver']}")
    print(f"   Seeded {len(AMBULANCES)} ambulances.")


if __name__ == '__main__':
    print("🔥  EHVRM Firestore Seeder")
    print("   Project:", os.getenv('GCLOUD_PROJECT', '(from serviceAccountKey)'))
    seed_hospitals()
    seed_ambulances()
    print("\n✅  Done! Check Firebase Console → Firestore to verify the data.\n")
