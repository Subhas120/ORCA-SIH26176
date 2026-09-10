# ORCA — M3 + M4 Complete Prototype

This implementation follows the M3 (Weather, Safety & Risk) and M4 (GIS & Route Optimization)
sections of the ORCA SIH26176 Master Project Execution Plan.

## M3
- Weather Agent with a fixed JSON contract
- Deterministic weighted Risk Engine
- Risk bands: LOW 0–25, MODERATE 26–50, HIGH 51–79, EXTREME 80–100
- Safety overrides:
  - severe official cyclone warning -> EXTREME
  - dangerous wave -> configurable HIGH/EXTREME floor
  - restricted zone -> DO NOT ENTER
- Reasons/evidence are always returned
- Missing weather fields can use cached values with reduced confidence

## M4
- Latitude/longitude distance using Haversine
- GeoJSON Point/Polygon handling
- Point-in-polygon geofencing with Shapely
- Nearest PFZ ranking
- Risk-aware A* routing
- Restricted cells are blocked
- Route cost = distance + weather risk + wave risk + restricted-zone penalty + hazard penalty

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python demo.py
pytest -q
```

This is a prototype. The PDF explicitly says the risk weights/bands are engineering
assumptions for a prototype, not universal scientific thresholds. Replace/configure them
with domain-expert or historical-data calibration before operational use.


## Git workflow

See `TEAM_GIT_SETUP.md`.

M3 branch:
```cmd
feature/m3-risk
```

M4 branch:
```cmd
feature/m4-gis
```

## Common project structure

See `COMMON_STRUCTURE.md` and run:

```cmd
create_structure.bat
```

## Data contracts

See `data_contracts.json`.

M1 -> downstream:
```json
{
  "intent": "SAFETY_CHECK",
  "location": "Kochi",
  "date": "tomorrow",
  "time": "morning",
  "activity": "fishing"
}
```

M3 and M4 should consume structured data and return stable JSON contracts so M5 can integrate
them without changing their internal implementation.
