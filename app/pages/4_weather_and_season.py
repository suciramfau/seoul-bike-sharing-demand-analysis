import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
from utils import (
    load_data,
    harmonize_columns,
    standardize_types,
    filter_functioning_days,
    add_time_features,
    COL,
    validate_required_columns,
)

st.title("4) Weather & Season")
st.caption("Understand how external factors (season and weather) relate to rental demand.")

data_path = st.session_state.get("data_path", "data/seoulbike_cleaned.csv")
apply_filter = st.session_state.get("apply_filter", True)

df = load_data(data_path)
df = harmonize_columns(df)
df = standardize_types(df)
if apply_filter:
    df = filter_functioning_days(df)
df = add_time_features(df)

validate_required_columns(df, ["target", "season", "date"])

st.subheader("Average rentals by season")
season_avg = df.groupby(COL["season"])[COL["target"]].mean().sort_values(ascending=False)
st.bar_chart(season_avg)

st.markdown("---")

st.subheader("Monthly trend (average rentals)")
if "Month" in df.columns and df["Month"].notna().any():
    monthly = df.groupby("Month")[COL["target"]].mean().sort_index()
    st.line_chart(monthly)
else:
    st.info("Month feature is unavailable because Date column could not be parsed.")

st.markdown("---")

# Optional: Weather proxy using Rainfall/Snowfall if available
weather_cols_available = [c for c in [COL["rainfall"], COL["snowfall"]] if c in df.columns]
if weather_cols_available:
    st.subheader("Weather effect (Rainfall / Snowfall)")
    col1, col2 = st.columns(2)

    if COL["rainfall"] in df.columns:
        with col1:
            st.write("Avg rentals by Rainfall bucket")
            bucket = pd.cut(df[COL["rainfall"]].fillna(0), bins=[-0.01, 0, 5, 20, 1000], labels=["0", "0-5", "5-20", ">20"])
            rain_avg = df.groupby(bucket)[COL["target"]].mean()
            st.bar_chart(rain_avg)

    if COL["snowfall"] in df.columns:
        with col2:
            st.write("Avg rentals by Snowfall bucket")
            bucket = pd.cut(df[COL["snowfall"]].fillna(0), bins=[-0.01, 0, 1, 5, 1000], labels=["0", "0-1", "1-5", ">5"])
            snow_avg = df.groupby(bucket)[COL["target"]].mean()
            st.bar_chart(snow_avg)
else:
    st.info("Weather columns (Rainfall/Snowfall) are not available in this dataset.")
