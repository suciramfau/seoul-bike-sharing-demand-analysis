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

st.title("2) Demand Patterns")
st.caption("Peak hour behavior and time-based demand patterns.")

data_path = st.session_state.get("data_path", "data/seoulbike_cleaned.csv")
apply_filter = st.session_state.get("apply_filter", True)

df = load_data(data_path)
df = harmonize_columns(df)
df = standardize_types(df)
if apply_filter:
    df = filter_functioning_days(df)
df = add_time_features(df)

validate_required_columns(df, ["target", "hour", "date"])

st.subheader("Average rentals by hour")
hourly = df.groupby(COL["hour"])[COL["target"]].mean().sort_index()
st.line_chart(hourly)

peak_hour = int(hourly.idxmax())
peak_val = float(hourly.max())

c1, c2, c3 = st.columns(3)
c1.metric("Peak Hour", f"{peak_hour:02d}:00")
c2.metric("Avg Rentals at Peak", f"{peak_val:.0f}")
c3.metric("Avg Rentals (All Hours)", f"{df[COL['target']].mean():.0f}")

st.markdown("---")
st.subheader("TimeSlot breakdown")
slot = df.groupby("TimeSlot")[COL["target"]].mean().sort_values(ascending=False)
st.bar_chart(slot)

st.markdown("---")
st.subheader("Daily total rentals trend")
daily = df.groupby(df[COL["date"]].dt.date)[COL["target"]].sum()
st.line_chart(daily)

with st.expander("Supporting table (hourly averages)"):
    st.dataframe(hourly.rename("avg_rentals").to_frame(), use_container_width=True)
