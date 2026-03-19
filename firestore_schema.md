# Firestore Database Schema
# EHVRM-System — Emergency Hospital Vehicle Routing & Management

## Collections

---

### 📁 emergencies
Logged every time the Emergency Router finds a route.

```
emergencies/
  {auto-id}/
    id           : "EMR-0001"         (string)
    condition    : "Cardiac Arrest"   (string)
    severity     : "Critical"         (string)
    hospital     : "AIIMS Jodhpur"    (string — name of top recommendation)
    hospital_id  : 1                  (number)
    patient_lat  : 26.292             (number)
    patient_lng  : 73.014             (number)
    eta_min      : 8                  (number)
    distance_km  : 3.2                (number)
    time         : "14:32:10"         (string)
    status       : "Dispatched"       (string — Dispatched | Arrived | Resolved)
    createdAt    : Timestamp          (Firestore server timestamp)
```

---

### 📁 alerts
Logged every time a pre-alert is sent to a hospital.

```
alerts/
  {auto-id}/
    hospital_id   : 1                 (number)
    hospital_name : "AIIMS Jodhpur"   (string)
    condition     : "Cardiac Arrest"  (string)
    eta_min       : 8                 (number)
    emergency_id  : "EMR-0001"        (string — links back to emergencies)
    sentAt        : Timestamp
```

---

### 📁 hospitals
Live bed availability pushed by hospital management.

```
hospitals/
  "1"/                               ← document ID = hospital ID as string
    available_beds  : 58             (number)
    icu_available   : 12             (number)
    trauma_available: 9              (number)
    burn_available  : 5              (number)
    er_wait_min     : 18             (number)
    status          : "Available"    (string — Available | Full | Partial)
    last_updated    : Timestamp
```

---

### 📁 ambulances
Live GPS positions pushed by ambulance driver app.

```
ambulances/
  "AMB-001"/
    lat    : 26.295                  (number)
    lng    : 73.019                  (number)
    status : "Available"             (string — Available | On Duty | Offline)
    driver : "Ramesh Kumar"          (string)
    phone  : "+91-9876543210"        (string)
    ts     : Timestamp               (last GPS ping)
```

---

## Firestore Security Rules (paste in Firebase Console → Firestore → Rules)

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Allow backend service account full access (handled by Admin SDK)
    // Allow frontend to READ hospitals and ambulances
    match /hospitals/{doc} {
      allow read: if true;
      allow write: if false; // only backend writes
    }
    match /ambulances/{doc} {
      allow read: if true;
      allow write: if false;
    }
    // Frontend can write emergencies and alerts (for direct Firestore logging)
    match /emergencies/{doc} {
      allow read, write: if true; // tighten with Auth in production
    }
    match /alerts/{doc} {
      allow read, write: if true;
    }
  }
}
```

---

## Indexes needed (auto-created when you first query)

- emergencies: createdAt DESC
- ambulances:  ts DESC
