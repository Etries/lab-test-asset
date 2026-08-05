# Battery Inventory

A small local web app to manage a battery inventory across many sites: track
each battery, its movements between sites, its health readings over time, and
per-site power outages.

It stores everything as plain CSV files (in `data/`) — no database to install.

---

## What you edit vs what you don't

- **`config.py`** — this is your file. App name, port, health-band thresholds,
  the list of battery/outage fields, statuses, move reasons. Change things here
  and restart the app. You rarely need anything else.
- `app.py`, `data_store.py`, `templates/`, `static/` — the machinery. Leave these
  alone unless you want to change behaviour or looks.

---

## Running it (the full workflow)

These are the exact steps for: put on GitHub → clone → virtual environment → run.

### 1. First time, on the PC where you build it

```bash
cd battery-app
python3 -m venv venv                 # create a virtual environment
source venv/bin/activate             # (Linux/Mac)  -> on Windows: venv\Scripts\activate
pip install -r requirements.txt      # install Flask + openpyxl
python app.py                        # starts the app, opens your browser
```

The app runs at **http://127.0.0.1:5000** (change the port in `config.py`).
Press **Ctrl+C** to stop.

### 2. Put it on GitHub

```bash
git init
git add .
git commit -m "Battery inventory app"
git branch -M main
git remote add origin https://github.com/YOUR-NAME/battery-app.git
git push -u origin main
```

`.gitignore` already excludes the virtual environment and the auto-backups.
Your `data/*.csv` files **are** committed, so your data travels with the repo.
(If you don't want data in GitHub, add `data/*.csv` to `.gitignore` before the
first commit.)

### 3. On another machine: download and run

```bash
git clone https://github.com/YOUR-NAME/battery-app.git
cd battery-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

## Loading your real data

The app starts with the sample CSVs in `data/`. To load your own cleaned
workbook (with sheets Batteries, Movements, Readings, Outages, Sites):

```bash
python import_from_excel.py path/to/cleaned_workbook.xlsx
```

This overwrites the matching CSVs (a backup is taken first).

---

## How the data is organised

Five CSV files in `data/`:

| File | One row per… |
|------|--------------|
| `batteries.csv` | battery (its current state) |
| `movements.csv` | move between sites |
| `readings.csv`  | health reading (voltage / SoH at a point in time) |
| `outages.csv`   | power outage at a site |
| `sites.csv`     | site |

Current state lives on the battery; history lives in the other tables. When you
record a move, the app updates the battery **and** adds a movement row, so the
two never disagree.

---

## Safety notes

- Every save writes a timestamped backup into `data/backups/` (last 40 kept).
- **Don't open a CSV in Excel while the app is running** — Excel locks the file
  and can silently reformat dates. Treat the app as the only editor.
