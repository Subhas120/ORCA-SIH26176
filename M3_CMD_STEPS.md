# M3 — Weather, Safety & Risk — CMD Steps

## 1. Clone and create your branch

```cmd
git clone https://github.com/Subhas120/ORCA-SIH26176.git ORCA-M3
cd ORCA-M3
git switch -c feature/m3-risk
git push -u origin feature/m3-risk
```

Verify:

```cmd
git branch
```

You should see:

```text
* feature/m3-risk
  main
```

## 2. Create the common folders

Copy `create_structure.bat` into the repo or use the commands in it:

```cmd
create_structure.bat
```

## 3. Create Python environment

```cmd
python -m venv .venv
.venv\Scripts\activate
```

## 4. Install M3 dependencies

```cmd
pip install -r requirements.txt
```

## 5. M3 implementation order

Build in this order:

1. Weather Agent
2. Normalize weather data
3. Risk component calculation
4. Weighted Risk Engine
5. Risk classification
6. Safety overrides
7. Reasons/evidence
8. Confidence
9. Risk timeline
10. Tests

## 6. Run M3 tests

```cmd
pytest tests/test_m3.py -q
```

## 7. Run the demo

```cmd
python demo.py
```

## 8. Save your work

```cmd
git status
git add .
git commit -m "M3: implement weather and deterministic risk engine"
git push
```

Do not merge into main yourself.

## M3 rules from the execution plan

Weights:
- Wave 25%
- Official warning 25%
- Wind 20%
- Rain/visibility 10%
- Sea state/current 10%
- Location/zones 10%

Bands:
- 0-25 LOW
- 26-50 MODERATE
- 51-79 HIGH
- 80-100 EXTREME

Overrides:
- Severe official cyclone warning -> EXTREME
- Dangerous wave -> HIGH/EXTREME floor
- Restricted marine zone -> DO NOT ENTER

The weights and bands are prototype engineering assumptions, not universal scientific thresholds.
