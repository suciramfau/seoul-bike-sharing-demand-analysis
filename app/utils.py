from __future__ import annotations

import os
from typing import Dict, List

import pandas as pd
import streamlit as st


# Canonical column keys used throughout the app
# You can adjust these canonical names, but keep the keys stable.
COL: Dict[str, str] = {
    "date": "Date",
    "target": "Rented Bike Count",
    "hour": "Hour",
    "season": "Seasons",
    "holiday": "Holiday",
    "functioning_day": "Functioning Day",
    # optional / sometimes present:
    "temp": "Temperature(°C)",
    "humidity": "Humidity(%)",
    "wind": "Wind speed (m/s)",
    "visibility": "Visibility (10m)",
    "dew_point": "Dew point temperature(°C)",
    "solar": "Solar Radiation (MJ/m2)",
    "rainfall": "Rainfall(mm)",
    "snowfall": "Snowfall (cm)",
}


def _norm(s: str) -> str:
    """Normalize a column name for fuzzy matching."""
    return (
        str(s)
        .strip()
        .lower()
        .replace("(", "")
        .replace(")", "")
        .replace("°", "")
        .replace("%", "")
        .replace("/", " ")
        .replace("-", " ")
        .replace("__", "_")
        .replace("  ", " ")
        .replace("_", " ")
        .replace(".", " ")
        .replace(",", " ")
        .replace(":", " ")
        .strip()
    )


def _build_normalized_lookup(columns: List[str]) -> Dict[str, str]:
    """Map normalized -> original column name."""
    lookup: Dict[str, str] = {}
    for c in columns:
        lookup[_norm(c)] = c
    return lookup


def harmonize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Align common variations of column names to canonical names in COL.
    This prevents KPI 'N/A' caused by mismatched column labels.
    """
    df = df.copy()

    # strip whitespace in columns
    df.columns = [str(c).strip() for c in df.columns]
    lookup = _build_normalized_lookup(list(df.columns))

    # Define candidates for each canonical field (normalized forms)
    candidates = {
        "date": [
            "date",
            "datetime",
            "timestamp",
        ],
        "target": [
            "rented bike count",
            "rentedbikecount",
            "rented_bike_count",
            "rent bike count",
            "rentbikecount",
            "bike count",
            "bike rental count",
            "rental count",
            "count",
        ],
        "hour": ["hour", "hr"],
        "season": ["seasons", "season"],
        "holiday": ["holiday", "is holiday", "is_holiday"],
        "functioning_day": ["functioning day", "functioningday", "operating day", "operational day"],
        "temp": ["temperature c", "temperature", "temp c", "temp"],
        "humidity": ["humidity", "humidity percent"],
        "wind": ["wind speed m s", "wind speed", "windspeed"],
        "visibility": ["visibility 10m", "visibility"],
        "dew_point": ["dew point temperature c", "dew point temperature", "dew point"],
        "solar": ["solar radiation mj m2", "solar radiation"],
        "rainfall": ["rainfall mm", "rainfall"],
        "snowfall": ["snowfall cm", "snowfall"],
    }

    rename_map: Dict[str, str] = {}

    for key, canon in COL.items():
        if canon in df.columns:
            continue  # already canonical

        # try candidate matches
        for cand in candidates.get(key, []):
            cand_norm = _norm(cand)
            if cand_norm in lookup:
                rename_map[lookup[cand_norm]] = canon
                break

        # special handling: some datasets use underscores heavily
        if canon not in df.columns:
            # try exact normalized match of the canonical name itself
            canon_norm = _norm(canon)
            if canon_norm in lookup and lookup[canon_norm] != canon:
                rename_map[lookup[canon_norm]] = canon

    if rename_map:
        df = df.rename(columns=rename_map)

    return df


def standardize_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize datatypes (date parsing, numerics, categoricals).
    Safe even if some optional columns are missing.
    """
    df = df.copy()

    # Date
    if COL["date"] in df.columns:
        df[COL["date"]] = pd.to_datetime(df[COL["date"]], errors="coerce", dayfirst=True)

    # Numerics: try to coerce commonly numeric fields
    numeric_cols = [
        COL["target"], COL["hour"],
        COL["temp"], COL["humidity"], COL["wind"], COL["visibility"], COL["dew_point"],
        COL["solar"], COL["rainfall"], COL["snowfall"],
    ]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Categoricals: strip/normalize strings
    for c in [COL["season"], COL["holiday"], COL["functioning_day"]]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()

    return df


def filter_functioning_days(df: pd.DataFrame) -> pd.DataFrame:
    """Filter Functioning Day == Yes (robust to Yes/No variants)."""
    df = df.copy()
    col = COL["functioning_day"]
    if col not in df.columns:
        return df

    s = df[col].astype(str).str.strip().str.lower()
    yes_values = {"yes", "y", "true", "1"}
    return df[s.isin(yes_values)]


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add Month, DayOfWeek, IsWeekend, TimeSlot."""
    df = df.copy()

    if COL["date"] in df.columns:
        dt = df[COL["date"]]
        df["Month"] = dt.dt.month
        df["DayOfWeek"] = dt.dt.day_name()
        df["IsWeekend"] = dt.dt.weekday >= 5
    else:
        # fallback columns if date not present
        df["Month"] = pd.NA
        df["DayOfWeek"] = pd.NA
        df["IsWeekend"] = pd.NA

    if COL["hour"] in df.columns:
        h = df[COL["hour"]].fillna(-1).astype(int)

        def _timeslot(x: int) -> str:
            if 7 <= x <= 9:
                return "Morning Peak (07-09)"
            if 17 <= x <= 19:
                return "Evening Peak (17-19)"
            if 10 <= x <= 16:
                return "Midday (10-16)"
            if 20 <= x <= 23:
                return "Night (20-23)"
            if 0 <= x <= 6:
                return "Early Morning (00-06)"
            return "Unknown"

        df["TimeSlot"] = h.map(_timeslot)
    else:
        df["TimeSlot"] = "Unknown"

    return df


@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    """Load CSV with basic safety checks."""
    if not path:
        st.error("Dataset path is empty.")
        st.stop()

    if not os.path.exists(path):
        st.error(f"Dataset not found at: {path}")
        st.stop()

    try:
        df = pd.read_csv(path)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        st.stop()

    return df


def validate_required_columns(df: pd.DataFrame, required_keys: List[str]) -> None:
    """
    Ensure required canonical columns exist.
    required_keys are keys in COL, e.g. ["date", "target", "hour"].
    Stops the page if missing.
    """
    missing = []
    for k in required_keys:
        if k not in COL:
            missing.append(f"(unknown key) {k}")
            continue
        canon = COL[k]
        if canon not in df.columns:
            missing.append(f"{k} -> '{canon}'")

    if missing:
        st.error(
            "Required columns are missing after harmonization:\n\n- "
            + "\n- ".join(missing)
            + "\n\nOpen 'Column list' expander to see detected columns."
        )
        st.stop()
