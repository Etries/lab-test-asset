# =============================================================================
#  CONFIG.PY  -  This is YOUR file. Almost everything you'll want to change
#  lives here. You should rarely need to open the other .py files.
#
#  After editing this file, just restart the app (Ctrl+C then `python app.py`).
# =============================================================================

# -----------------------------------------------------------------------------
# 1. WHERE THE DATA LIVES
#    The app stores everything as CSV files in this folder. Point this at a
#    shared folder if you like. Keep the trailing slash off; use forward slashes
#    even on Windows (Python is fine with that).
# -----------------------------------------------------------------------------
DATA_DIR = "data"

# Every time the app saves, it first writes a timestamped copy here, so a bad
# edit is always recoverable. Old backups are pruned to the newest N.
BACKUP_DIR = "data/backups"
KEEP_BACKUPS = 40

# The app keeps this shared workbook in sync with the data on every change, so
# anyone can open it to read or take a copy. The app stays the editor; to bring
# hand-edits back in, use the Import button in the app.
WORKBOOK_FILE = "data/battery_inventory.xlsx"
SYNC_WORKBOOK = True        # set False to stop auto-updating the .xlsx

# -----------------------------------------------------------------------------
# 2. THE APP'S NAME + WHICH PORT IT RUNS ON
#    Open http://127.0.0.1:<PORT> in your browser after starting.
# -----------------------------------------------------------------------------
APP_TITLE = "Battery Inventory"
COMPANY_NAME = "Your Company"
PORT = 5000

# -----------------------------------------------------------------------------
# 3. HEALTH BANDS
#    A battery's SoH% is bucketed into one of these bands for filtering and the
#    coloured dot. Edit the numbers to re-tune what "healthy" means. Bands are
#    checked top to bottom; the first one whose `min` the SoH meets wins.
#    `key` is used internally (don't use spaces); `label` is what you see;
#    `colour` is any CSS colour.
# -----------------------------------------------------------------------------
HEALTH_BANDS = [
    {"key": "healthy", "label": "Healthy",  "min": 80, "colour": "#2e9e5b"},   # green
    {"key": "watch",   "label": "Watch",    "min": 60, "colour": "#d9a406"},   # amber
    {"key": "replace", "label": "Replace",  "min": 0,  "colour": "#c8442f"},   # red
]
# Batteries with no SoH recorded get this band:
HEALTH_UNKNOWN = {"key": "unknown", "label": "Unknown", "colour": "#8a8f98"}

# -----------------------------------------------------------------------------
# 4. STATUS + REASON VOCABULARIES
#    STATUSES are the allowed states a battery can be in.
#    MOVEMENT_REASONS appear in the "Move battery" dropdown. Each reason can
#    optionally force a status via SETS_STATUS (leave as None to keep current).
# -----------------------------------------------------------------------------
STATUSES = ["Active", "In Storage", "Faulty", "Under Test", "Decommissioned"]

MOVEMENT_REASONS = [
    {"reason": "New Install",        "sets_status": "Active"},
    {"reason": "Redeployment",       "sets_status": "Active"},
    {"reason": "Fault Replacement",  "sets_status": "Faulty"},
    {"reason": "To Storage",         "sets_status": "In Storage"},
    {"reason": "From Storage",       "sets_status": "Active"},
    {"reason": "Decommission",       "sets_status": "Decommissioned"},
    {"reason": "Other",              "sets_status": None},
]

# Sites with these names get special treatment in the site dropdowns / views.
# (They still behave like normal sites otherwise.)
STORAGE_SITE = "Stock"
DECOMMISSION_SITE = "Recycled"

# -----------------------------------------------------------------------------
# 5. THE BATTERY FIELDS
#    This defines the columns of the battery record AND how the forms are built.
#    To ADD a field: add a line here, and it automatically appears in the table,
#    the detail page, and the new/edit form. No other file needs changing.
#
#      key      : column name in the CSV (no spaces)
#      label    : shown in the UI
#      type     : "text" | "number" | "date" | "choice"
#      choices  : only for type "choice" — either a list, or the name of a list
#                 defined elsewhere ("STATUSES", "SITES", "BRANDS")
#      required : if True, the new-entry form won't save without it
#      in_table : show this column in the main battery list?
# -----------------------------------------------------------------------------
BATTERY_FIELDS = [
    {"key": "battery_id",       "label": "Battery Nickname","type": "text",   "required": True,  "in_table": True},
    {"key": "brand",            "label": "Brand",          "type": "choice", "choices": "BRANDS", "in_table": True},
    {"key": "model",            "label": "Model",          "type": "text",   "in_table": False},
    {"key": "supplier",         "label": "Supplier",       "type": "text",   "in_table": False},
    {"key": "delivery_date",    "label": "Delivery date",  "type": "date",   "in_table": False},
    # --- the four measurement columns, in the same order as the printed sheet ---
    {"key": "capacity_ah",      "label": "Capacity/Ah",    "type": "number", "in_table": False},
    {"key": "tested_voltage",   "label": "Tested voltage", "type": "number", "in_table": False},
    {"key": "internal_res_mohm","label": "Internal resistance","type": "number","in_table": False},
    {"key": "tested_capacity",  "label": "Tested capacity","type": "number", "in_table": False},
    {"key": "soh_pct",          "label": "SoH",            "type": "number", "in_table": True},
    # ---------------------------------------------------------------------------
    {"key": "current_site",     "label": "Current site",   "type": "choice", "choices": "SITES", "in_table": True},
    {"key": "action",           "label": "Action",         "type": "text",   "in_table": False},
    {"key": "remarks",          "label": "Remark",         "type": "text",   "in_table": False},
    {"key": "date_fitted",      "label": "Date fitted",    "type": "date",   "in_table": False},
    {"key": "last_moved_date",  "label": "Last moved date","type": "date",   "in_table": False},
    {"key": "previous_site",    "label": "Previous site",  "type": "text",   "in_table": False},
    {"key": "status",           "label": "Status",         "type": "choice", "choices": "STATUSES", "in_table": True},
]

# The single field that uniquely identifies a battery (must match one key above).
BATTERY_ID_FIELD = "battery_id"

# The field holding SoH% (used for the health band). Must match a key above.
SOH_FIELD = "soh_pct"

# -----------------------------------------------------------------------------
# 6. OUTAGE FIELDS  (same idea as battery fields, for the power-outage log)
# -----------------------------------------------------------------------------
OUTAGE_FIELDS = [
    {"key": "site_id",            "label": "Site",              "type": "choice", "choices": "SITES", "required": True},
    {"key": "outage_date",        "label": "Date",              "type": "date",   "required": True},
    {"key": "start_time",         "label": "Start time",        "type": "text"},
    {"key": "duration_hours",     "label": "Duration (hours)",  "type": "number"},
    {"key": "site_shut_down",     "label": "Site shut down?",   "type": "choice", "choices": ["Yes", "No"]},
    {"key": "devices_off",        "label": "Devices switched off?", "type": "choice", "choices": ["Yes", "No"]},
    {"key": "voltage_when_back",  "label": "Voltage when back", "type": "number"},
    {"key": "remarks",            "label": "Remarks",           "type": "text"},
]

# -----------------------------------------------------------------------------
# 7. READING FIELDS  (a health reading recorded over time)
# -----------------------------------------------------------------------------
READING_FIELDS = [
    {"key": "battery_id",   "label": "Battery",  "type": "choice", "choices": "BATTERIES", "required": True},
    {"key": "reading_date", "label": "Date",     "type": "date",   "required": True},
    {"key": "voltage",      "label": "Voltage",  "type": "number"},
    {"key": "soh_pct",      "label": "SoH %",    "type": "number"},
    {"key": "source",       "label": "Source",   "type": "choice", "choices": ["Manual", "Audit", "Cacti Import", "SNMP"]},
]

# -----------------------------------------------------------------------------
# 8. SITE FIELDS
# -----------------------------------------------------------------------------
SITE_FIELDS = [
    {"key": "site_id",         "label": "Site ID",       "type": "text", "required": True},
    {"key": "region",          "label": "Region",        "type": "text"},
    {"key": "power_setup",     "label": "Power setup",    "type": "text"},
    {"key": "grid_available",  "label": "Grid available", "type": "choice", "choices": ["Yes", "No"]},
]

# =============================================================================
#  END OF CONFIG. You normally don't need to edit anything below this in any file.
# =============================================================================
