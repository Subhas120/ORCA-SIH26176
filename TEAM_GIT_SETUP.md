# ORCA SIH26176 — Git Setup

Repository:
https://github.com/Subhas120/ORCA-SIH26176

## Everyone

```cmd
git clone https://github.com/Subhas120/ORCA-SIH26176.git
cd ORCA-SIH26176
git branch
git status
```

Do NOT work directly on `main`.

## Branches from the Master Execution Plan

M1:
```cmd
git switch -c feature/m1-ai
git push -u origin feature/m1-ai
```

M2:
```cmd
git switch -c feature/m2-marine
git push -u origin feature/m2-marine
```

M3:
```cmd
git switch -c feature/m3-risk
git push -u origin feature/m3-risk
```

M4:
```cmd
git switch -c feature/m4-gis
git push -u origin feature/m4-gis
```

M5:
```cmd
git switch -c feature/m5-backend
git push -u origin feature/m5-backend
```

M6:
```cmd
git switch -c feature/m6-frontend
git push -u origin feature/m6-frontend
```

After creating the assigned branch:

```cmd
git branch
```

Send the output to the team.

## If M3 and M4 are being done by the same person

Do NOT try to work on two branches simultaneously in one working directory.

Option A — recommended: use two clones.

M3 clone:
```cmd
git clone https://github.com/Subhas120/ORCA-SIH26176.git ORCA-M3
cd ORCA-M3
git switch -c feature/m3-risk
git push -u origin feature/m3-risk
```

M4 clone:
```cmd
git clone https://github.com/Subhas120/ORCA-SIH26176.git ORCA-M4
cd ORCA-M4
git switch -c feature/m4-gis
git push -u origin feature/m4-gis
```

Option B — one clone:
Commit/stash your work before switching:

```cmd
git status
git add .
git commit -m "M3: save current work"
git switch feature/m4-gis
```

## Team rule

```text
                    ORCA GitHub
                         |
                       main
                         |
          +--------------+--------------+
          |              |              |
        Pod A           Pod B          Pod C
       M1 + M2         M3 + M4        M5 + M6
          |              |              |
      own branches   own branches   own branches
```

For the initial setup, do not merge feature branches. First agree on:
1. common folder structure
2. data contracts
3. ownership
4. how each module is run/tested

Then integrate through reviewed pull requests.

## Important

The Master Execution Plan explicitly requires one Git branch per feature:
feature/m1-ai, feature/m2-marine, feature/m3-risk, feature/m4-gis,
feature/m5-backend, feature/m6-frontend.

Before merging:
Code -> Test -> Partner Review -> Merge.

Never directly edit another member's module.
