# ==========================================
# SecureCheck ETL Pipeline
# ==========================================

# ------------------------------------------
# Import Libraries
# ------------------------------------------

import pandas as pd
import sqlite3

from pathlib import Path


# ==========================================
# FILE PATH CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

RAW_DATA_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "traffic_stops.xlsx"
)

PROCESSED_DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "cleaned_traffic_stops.csv"
)

DB_FILE = BASE_DIR / "securecheck.db"


# ==========================================
# CHECK RAW FILE EXISTS
# ==========================================

if not RAW_DATA_FILE.exists():

    raise FileNotFoundError(
        f"Raw file not found:\n{RAW_DATA_FILE}"
    )


# ==========================================
# EXTRACT
# ==========================================

print("Loading Excel dataset...")

df = pd.read_excel(RAW_DATA_FILE)

print(f"Rows Loaded: {len(df)}")


# ==========================================
# TRANSFORM
# ==========================================

print("Cleaning dataset...")


# ------------------------------------------
# Convert Date Column
# ------------------------------------------

df["stop_date"] = pd.to_datetime(
    df["stop_date"],
    errors="coerce"
).dt.date


# ------------------------------------------
# Clean Time Column
# ------------------------------------------

df["stop_time"] = (
    df["stop_time"]
    .astype(str)
    .str.split(".")
    .str[0]
)


# ------------------------------------------
# Standardize Gender Values
# ------------------------------------------

df["driver_gender"] = (
    df["driver_gender"]
    .astype(str)
    .str.strip()
    .str.lower()
)

df.loc[
    df["driver_gender"].isin(["male", "m"]),
    "driver_gender"
] = "M"

df.loc[
    df["driver_gender"].isin(["female", "f"]),
    "driver_gender"
] = "F"


# ------------------------------------------
# Keep Valid Genders Only
# ------------------------------------------

df = df[
    df["driver_gender"].isin(["M", "F"])
]


# ------------------------------------------
# Clean Vehicle Numbers
# ------------------------------------------

df["vehicle_number"] = (
    df["vehicle_number"]
    .astype(str)
    .str.strip()
    .str.upper()
)


# ------------------------------------------
# Convert Boolean Columns
# ------------------------------------------

boolean_columns = [
    "search_conducted",
    "is_arrested",
    "drugs_related_stop"
]

for col in boolean_columns:

    df[col] = (
        df[col]
        .fillna(0)
        .astype(int)
    )


# ------------------------------------------
# Remove Important Missing Values
# ------------------------------------------

df = df.dropna(
    subset=[
        "stop_date",
        "stop_time",
        "vehicle_number",
        "violation",
        "driver_age",
        "stop_duration"
    ]
)


# ------------------------------------------
# Remove Duplicate Records
# ------------------------------------------

df = df.drop_duplicates()


print(f"Rows After Cleaning: {len(df)}")


# ==========================================
# SAVE CLEANED CSV
# ==========================================

print("Saving cleaned CSV...")

df.to_csv(
    PROCESSED_DATA_FILE,
    index=False
)


# ==========================================
# LOAD CLEANED CSV
# ==========================================

print("Loading cleaned CSV...")

cleaned_df = pd.read_csv(
    PROCESSED_DATA_FILE
)


# ==========================================
# LOAD TO SQLITE DATABASE
# ==========================================

print("Creating SQLite database...")

conn = sqlite3.connect(DB_FILE)

cleaned_df.to_sql(
    "traffic_stops",
    conn,
    if_exists="replace",
    index=False
)

conn.close()


# ==========================================
# SUCCESS MESSAGE
# ==========================================

print("ETL Pipeline Completed Successfully")

print(f"Database Created: {DB_FILE}")