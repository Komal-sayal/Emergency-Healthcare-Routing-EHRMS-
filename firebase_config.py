"""
database/firebase/firebase_config.py

HOW TO SET UP FIREBASE (one-time):
────────────────────────────────────────────────────────────
1. Go to https://console.firebase.google.com
2. Click "Add project" → name it "EHVRM-System"
3. Enable Google Analytics (optional)
4. In the left sidebar → Build → Firestore Database → Create database
   → Start in TEST MODE (for hackathon)
   → Choose region: asia-south1 (Mumbai, closest to Jodhpur)
5. In Project Settings → Service accounts → Generate new private key
   → Download as "serviceAccountKey.json"
   → Place it in: backend/database/firebase/serviceAccountKey.json
   → NEVER commit this file to Git! (already in .gitignore below)
────────────────────────────────────────────────────────────
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore

# Path to your downloaded service account key
SERVICE_ACCOUNT_PATH = os.path.join(
    os.path.dirname(__file__),
    "serviceAccountKey.json"
)

# Initialize only once
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()


# ── COLLECTION REFERENCES ────────────────────────────────────────────────────

def emergencies_col():
    """Returns reference to the 'emergencies' Firestore collection."""
    return db.collection("emergencies")

def alerts_col():
    """Returns reference to the 'alerts' Firestore collection."""
    return db.collection("alerts")

def hospitals_col():
    """Returns reference to the 'hospitals' Firestore collection."""
    return db.collection("hospitals")

def ambulances_col():
    """Returns reference to the 'ambulances' Firestore collection."""
    return db.collection("ambulances")


# ── HELPER FUNCTIONS ─────────────────────────────────────────────────────────

def log_emergency_to_firestore(emergency_data: dict) -> str:
    """
    Write an emergency dispatch record to Firestore.
    Returns the auto-generated document ID.

    Usage in routes/routing.py:
        from database.firebase.firebase_config import log_emergency_to_firestore
        doc_id = log_emergency_to_firestore({ ... })
    """
    doc_ref = emergencies_col().add(emergency_data)
    return doc_ref[1].id


def log_alert_to_firestore(alert_data: dict) -> str:
    """Write a pre-alert event to Firestore. Returns doc ID."""
    doc_ref = alerts_col().add(alert_data)
    return doc_ref[1].id


def get_recent_emergencies(limit: int = 20) -> list:
    """
    Fetch the most recent emergencies from Firestore, newest first.
    Replaces the in-memory EMERGENCIES list in production.
    """
    docs = (
        emergencies_col()
        .order_by("time", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def update_hospital_beds(hospital_id: int, available_beds: int, icu_available: int):
    """
    Update live bed counts for a hospital in Firestore.
    Call this from a hospital management portal to push real updates.
    """
    hospitals_col().document(str(hospital_id)).set({
        "available_beds": available_beds,
        "icu_available":  icu_available,
        "last_updated":   firestore.SERVER_TIMESTAMP,
    }, merge=True)


def update_ambulance_location(amb_id: str, lat: float, lng: float, status: str):
    """
    Update ambulance GPS position and status in Firestore.
    Call from the ambulance driver mobile app every 5 seconds.
    """
    ambulances_col().document(amb_id).set({
        "lat":    lat,
        "lng":    lng,
        "status": status,
        "ts":     firestore.SERVER_TIMESTAMP,
    }, merge=True)
