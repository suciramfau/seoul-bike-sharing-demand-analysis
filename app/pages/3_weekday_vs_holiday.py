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

st.title("3) Weekday vs Holiday")
st.caption("Compare demand patterns across holiday vs non-holiday and weekday/weekend behavior.")

data_path = st.session_state.get("data_path", "data/seoulbike_cleaned.csv")
apply_filter = st.session_state.get("apply_filter", True)

df = load_data(data_path)
df = harmonize_columns(df)
df = standardize_types(df)
if apply_filter:
    df = filter_functioning_days(df)
df = add_time_features(df)

validate_required_columns(df, ["target", "hour", "holiday", "date"])

# Normalize holiday values to two buckets
holiday_col = COL["holiday"]
s = df[holiday_col].astype(str).str.strip().str.lower()
df["_HolidayFlag"] = s.isin({"holiday", "yes", "true", "1", "y"})

st.subheader("Average rentals by hour (Holiday vs Non-Holiday)")
hourly = (
    df.groupby([COL["hour"], "_HolidayFlag"])[COL["target"]]
    .mean()
    .reset_index()
    .pivot(index=COL["hour"], columns="_HolidayFlag", values=COL["target"])
    .sort_index()
)
hourly.columns = ["Non-Holiday", "Holiday"] if len(hourly.columns) == 2 else [str(c) for c in hourly.columns]
st.line_chart(hourly)

st.markdown("---")

st.subheader("Overall rentals distribution (Holiday vs Non-Holiday)")
# Streamlit doesn't have native boxplot without extra libs; use summary stats
summary = df.groupby("_HolidayFlag")[COL["target"]].describe()[["count", "mean", "50%", "std", "min", "max"]]
summary.index = ["Non-Holiday", "Holiday"] if len(summary.index) == 2 else summary.index
st.dataframe(summary, use_container_width=True)

st.markdown("---")

st.subheader("Weekday vs Weekend (based on Date)")
if "IsWeekend" in df.columns:
    weekend_hourly = (
        df.groupby([COL["hour"], "IsWeekend"])[COL["target"]]
        .mean()
        .reset_index()
        .pivot(index=COL["hour"], columns="IsWeekend", values=COL["target"])
        .sort_index()
    )
    weekend_hourly.columns = ["Weekday", "Weekend"] if len(weekend_hourly.columns) == 2 else [str(c) for c in weekend_hourly.columns]
    st.line_chart(weekend_hourly)
else:
    st.info("Weekend features are unavailable because Date column could not be parsed.")
