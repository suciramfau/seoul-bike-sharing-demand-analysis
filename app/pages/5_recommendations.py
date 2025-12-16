import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from utils import (
    load_data,
    harmonize_columns,
    standardize_types,
    filter_functioning_days,
    add_time_features,
    COL,
    validate_required_columns,
)

st.title("5) Recommendations")
st.caption("Operational playbook and simple planning calculator (portfolio-friendly).")

data_path = st.session_state.get("data_path", "data/seoulbike_cleaned.csv")
apply_filter = st.session_state.get("apply_filter", True)

df = load_data(data_path)
df = harmonize_columns(df)
df = standardize_types(df)
if apply_filter:
    df = filter_functioning_days(df)
df = add_time_features(df)

validate_required_columns(df, ["target", "hour", "holiday", "season", "date"])

st.subheader("Actionable Insights (high-level)")
st.markdown(
    """
- **Increase bike availability during morning rush hours (07:00–09:00) on workdays.**
- **Run stronger promotions on clear-weather periods and targeted holiday time windows.**
- **Use weather forecasts (rain/snow signals) to proactively rebalance bikes.**
"""
)

st.markdown("---")
st.subheader("Simple Planner: Morning Peak Buffer (Workdays)")

# Build workday subset (Non-Holiday + Weekday)
holiday_col = COL["holiday"]
s = df[holiday_col].astype(str).str.strip().str.lower()
df["_HolidayFlag"] = s.isin({"holiday", "yes", "true", "1", "y"})

# Workday: Non-Holiday and not weekend (if possible)
workday_df = df[df["_HolidayFlag"] == False]
if "IsWeekend" in workday_df.columns:
    workday_df = workday_df[workday_df["IsWeekend"] == False]

# Focus hours 7-9
peak_df = workday_df[workday_df[COL["hour"]].between(7, 9)]
avg_peak = float(peak_df[COL["target"]].mean()) if len(peak_df) else float("nan")

if not (avg_peak == avg_peak):  # NaN check
    st.warning("Could not compute average demand during 07:00–09:00. Check Date/Hour parsing.")
    st.stop()

buffer_pct = st.slider("Buffer (%) to avoid stockouts", min_value=0, max_value=50, value=10, step=1)
recommended = avg_peak * (1 + buffer_pct / 100)
additional = recommended - avg_peak

c1, c2, c3 = st.columns(3)
c1.metric("Avg Peak Demand (07–09)", f"{avg_peak:,.0f}")
c2.metric("Recommended Availability", f"{recommended:,.0f}")
c3.metric("Additional Bikes", f"{additional:,.0f}")

st.info(
    "Note: This planner is simplified for portfolio purposes. In production, you would incorporate "
    "station-level constraints, fleet availability, and rebalancing logistics."
)
