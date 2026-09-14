# 🗽 NestMapper NYC

> **Know Before You Move** — A free NYC neighborhood intelligence guide

NestMapper NYC helps individuals and families find the most suitable neighborhood across New York City's five boroughs. Compare rent, transit, safety, schools, and disability accessibility — completely free and unbiased.

![NestMapper NYC](https://nestmapper.vercel.app)

---

## 🌐 Live Demo

- **Frontend:** [nestmapper.vercel.app](https://nestmapper.vercel.app)
- **API:** Coming soon on Railway

---

## 🚀 Features

- 🗺️ **Interactive Mapbox Map** — Color coded NYC neighborhood polygons
- 📊 **6 Dimension Scoring** — Affordability, Transit, Safety, Family, Accessibility, Convenience
- ⚖️ **Side by Side Compare** — Compare any two neighborhoods with radar charts
- 🎯 **Smart Recommendations** — Personalized matches based on your preferences
- ♿ **Accessibility Scoring** — First NYC tool with dedicated disability accessibility scores
- 🆓 **Completely Free** — No account required, no listing bias

---

## 🛠️ Tech Stack

**Frontend:**
- React + TypeScript + Vite
- Tailwind CSS
- Mapbox GL JS
- Recharts
- Axios

**Backend:**
- Python + Django
- Django REST Framework
- PostgreSQL
- Pandas + NumPy

**Data Sources:**
- NYC Open Data
- MTA API
- NYPD Crime Statistics
- NYC Department of Education

**Deployment:**
- Vercel (Frontend)
- Railway (Backend)

---

## ⚙️ How to Run Locally

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py compute_scores
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/neighborhoods/` | All neighborhoods |
| GET | `/api/neighborhoods/:id/` | Single neighborhood |
| GET | `/api/boroughs/:borough/` | By borough |
| GET | `/api/compare/?ids=1,2` | Compare two |
| POST | `/api/recommend/` | Get recommendations |

---

## 🗄️ Database Schema

8 relational tables:
- `Neighborhood` — Core neighborhood data
- `RentData` — Studio, 1BR, 2BR, 3BR prices
- `TransitInfo` — Subway lines and bus routes
- `SafetyData` — Crime statistics
- `Amenities` — Schools, parks, hospitals
- `AccessibilityData` — ADA and elevator data
- `ParkingData` — Parking difficulty and cost
- `NeighborhoodScore` — Computed scores

---

## 👥 Team

| Name | Role |
|------|------|
| Abu Bakar | Backend Developer |
| [Humam khan] | Frontend Developer |

Brooklyn College — CISC 4900 Capstone — Fall 2026

---

## 📝 License

MIT License — Free to use and learn from
