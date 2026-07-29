"""
data_store.py  -  Reads and writes the CSV files that hold all app data.

You normally won't edit this. It gives the rest of the app a simple way to load
a table (list of dict rows) and save it back safely:

  - saves are ATOMIC (write to a temp file, then rename) so a crash mid-save
    can't leave you with a half-written, corrupt CSV.
  - every save first drops a timestamped backup in the backups folder.

Each "table" is one CSV file: batteries.csv, movements.csv, readings.csv,
outages.csv, sites.csv
"""
import csv
import os
import shutil
import datetime
import config


def _path(table):
    return os.path.join(config.DATA_DIR, f"{table}.csv")


def _ensure_dirs():
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.BACKUP_DIR, exist_ok=True)


def load(table):
    """Return a list of row dicts for the given table (empty list if no file)."""
    path = _path(table)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_headers(table, default_fields):
    """Return the CSV's column names, or the configured defaults if no file yet."""
    path = _path(table)
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers:
                return headers
    return [f["key"] for f in default_fields]


def _backup(table):
    path = _path(table)
    if not os.path.exists(path):
        return
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = os.path.join(config.BACKUP_DIR, f"{table}.{stamp}.csv")
    shutil.copy2(path, dest)
    _prune_backups(table)


def _prune_backups(table):
    files = sorted(
        (f for f in os.listdir(config.BACKUP_DIR) if f.startswith(f"{table}.")),
        reverse=True,
    )
    for old in files[config.KEEP_BACKUPS:]:
        try:
            os.remove(os.path.join(config.BACKUP_DIR, old))
        except OSError:
            pass


def save(table, rows, headers):
    """Write rows (list of dicts) to the table's CSV, atomically, with a backup."""
    _ensure_dirs()
    _backup(table)
    path = _path(table)
    tmp = path + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h, "") for h in headers})
    os.replace(tmp, path)  # atomic on the same filesystem


def append(table, row, default_fields):
    """Convenience: load, add one row, save. Keeps existing headers."""
    rows = load(table)
    headers = load_headers(table, default_fields)
    # make sure any brand-new keys still get a column
    for k in row:
        if k not in headers:
            headers.append(k)
    rows.append(row)
    save(table, rows, headers)
    return rows
