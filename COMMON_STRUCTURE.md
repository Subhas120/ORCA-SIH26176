# ORCA SIH26176 — Common Folder Structure

The structure below follows the Master Execution Plan.

```text
ORCA/
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── maps/
│   └── services/
│
├── backend/
│   ├── main.py
│   ├── api/
│   ├── services/
│   ├── database/
│   └── models/
│
├── agents/
│   ├── intent/
│   ├── planner/
│   ├── ocean/
│   ├── weather/
│   ├── gis/
│   ├── risk/
│   └── explanation/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── geospatial/
│   ├── zones/
│   ├── routes/
│   └── geo_utils/
│
├── evaluation/
│   ├── test_cases/
│   ├── metrics/
│   └── reports/
│
├── docs/
│   ├── architecture/
│   ├── data_sources/
│   ├── api/
│   └── research/
│
├── requirements.txt
└── README.md
```

## M3 files

```text
agents/weather/weather_agent.py
agents/risk/risk_engine.py
```

## M4 files

```text
agents/gis/geo_utils.py
agents/gis/geofence.py
agents/gis/pfz.py
agents/gis/router.py
```

The existing prototype in this package follows the same conceptual structure.

## M1 -> downstream data contract

M1 should eventually produce a structured query such as:

```json
{
  "intent": "SAFETY_CHECK",
  "location": "Kochi",
  "date": "tomorrow",
  "time": "morning",
  "activity": "fishing"
}
```

M3/M4 should consume structured fields rather than parsing the user's sentence themselves.

## M3 -> M5/M1 contract

M3 risk output:

```json
{
  "risk_score": 34,
  "risk_level": "MODERATE",
  "reasons": [
    "Elevated wave conditions"
  ],
  "evidence": [],
  "confidence": "HIGH"
}
```

## M4 -> M5/M6 contract

Geofence:

```json
{
  "id": "zone-001",
  "name": "Restricted Zone",
  "type": "restricted",
  "inside": true,
  "penalty": 1000
}
```

PFZ:

```json
{
  "id": "PFZ-001",
  "name": "PFZ Alpha",
  "latitude": 9.95,
  "longitude": 76.30,
  "distance_km": 8.2
}
```

Route:

```json
{
  "found": true,
  "path": [[0,0], [0,1], [1,2]],
  "cost": 15.7,
  "steps": 3
}
```
