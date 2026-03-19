# 🚑 EHVRM-System — Emergency Hospital Vehicle Routing & Management

A full-stack emergency routing system for Jodhpur hospitals.
Built for hackathon — converts the single Python prototype into a proper
React frontend + Flask backend + Firebase database.

---

## 📁 Project Structure

```
EHVRM-System/
├── frontend/                    ← React + Vite app
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── utils/
│       │   ├── api.js           ← all axios API calls
│       │   └── firebase.js      ← Firestore frontend helpers
│       ├── styles/
│       │   └── globals.css      ← full design system
│       ├── components/
│       │   ├── Sidebar.jsx
│       │   └── Topbar.jsx
│       └── pages/
│           ├── Dashboard.jsx
│           ├── HospitalDirectory.jsx
│           ├── HospitalDetail.jsx
│           ├── EmergencyRouter.jsx
│           ├── AmbulanceTracker.jsx
│           ├── BudgetFinder.jsx
│           └── EmergencyLog.jsx
│
├── backend/                     ← Flask REST API
│   ├── app.py                   ← server entry point
│   ├── requirements.txt
│   ├── routes/
│   │   ├── hospitals.py         ← GET /api/hospitals, /api/hospital/<id>
│   │   ├── routing.py           ← POST /api/route
│   │   ├── ambulances.py        ← GET /api/ambulances
│   │   ├── emergencies.py       ← GET /api/emergencies, POST /api/alert
│   │   └── stats.py             ← GET /api/stats
│   ├── models/
│   │   └── hospital_data.py     ← all hospital records + ambulances
│   └── utils/
│       └── routing_engine.py    ← haversine, scoring, ETA
│
└── database/
    └── firebase/
        ├── firebase_config.py   ← Firestore Admin SDK helpers
        └── firestore_schema.md  ← collection structure + security rules
```

---

## 🚀 Quick Start

### 1 — Backend (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
# API running at http://localhost:5000
```

### 2 — Frontend (React)

```bash
cd frontend
npm install
npm run dev
# App running at http://localhost:5173
```

The Vite dev server proxies `/api/*` → `http://localhost:5000`
so you don't need to change any URLs.

---

## 🔑 APIs Needed

### 1. Firebase (Required for persistent storage)

| Step | Action |
|------|--------|
| 1 | Go to https://console.firebase.google.com |
| 2 | Create project → "EHVRM-System" |
| 3 | Build → Firestore Database → Create → Test mode → asia-south1 |
| 4 | Project Settings → Service accounts → Generate private key → save as `backend/database/firebase/serviceAccountKey.json` |
| 5 | Project Settings → Your apps → Add web app → copy config |
| 6 | Paste config into `frontend/src/utils/firebase.js` |

### 2. Google Maps JavaScript API (For map view in Ambulance Tracker)

| Step | Action |
|------|--------|
| 1 | Go to https://console.cloud.google.com |
| 2 | Create project → Enable "Maps JavaScript API" + "Geolocation API" |
| 3 | Credentials → Create API Key |
| 4 | Paste key into `frontend/src/pages/AmbulanceTracker.jsx` where marked |

### 3. Twilio SMS API (Optional — for real pre-alerts to hospital phones)

| Step | Action |
|------|--------|
| 1 | Sign up at https://twilio.com |
| 2 | Get Account SID + Auth Token + Phone number |
| 3 | Paste into `backend/routes/emergencies.py` where marked with `# TODO: Twilio` |
| 4 | `pip install twilio` |

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/hospitals | All hospitals with live bed data |
| GET | /api/hospital/:id | Single hospital detail |
| GET | /api/budget_hospitals | Hospitals grouped by budget tier |
| POST | /api/route | Emergency routing (body: lat, lng, condition, severity) |
| GET | /api/ambulances | Live ambulance fleet |
| GET | /api/emergencies | Last 20 emergency dispatches |
| GET | /api/stats | Dashboard summary stats |
| POST | /api/alert | Send pre-alert to hospital (body: hospital_id, condition, eta) |

---

## .gitignore

```
# Firebase credentials — NEVER commit
backend/database/firebase/serviceAccountKey.json
backend/.env

# Dependencies
frontend/node_modules/
__pycache__/
*.pyc
.env
```
