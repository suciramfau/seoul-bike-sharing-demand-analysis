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

st.title("1) Overview")
st.caption("Dataset snapshot, coverage, and core KPIs.")

# use global settings if set in app/app.py
data_path = st.session_state.get("data_path", "data/seoulbike_cleaned.csv")
apply_filter = st.session_state.get("apply_filter", True)

df = load_data(data_path)
df = harmonize_columns(df)
df = standardize_types(df)
if apply_filter:
    df = filter_functioning_days(df)
df = add_time_features(df)

validate_required_columns(df, ["date", "target", "hour", "season", "holiday"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{df.shape[0]:,}")
c2.metric("Total Rentals", f"{int(df[COL['target']].sum()):,}")
c3.metric("Avg Hourly Rentals", f"{df[COL['target']].mean():.0f}")
c4.metric("Max Hourly Rentals", f"{int(df[COL['target']].max()):,}")

st.markdown("---")

st.subheader("Dataset Coverage")
min_date = df[COL["date"]].min()
max_date = df[COL["date"]].max()
st.write(f"Date range: **{min_date.date()}** to **{max_date.date()}**")

col1, col2 = st.columns(2)
with col1:
    st.write("Season distribution")
    st.dataframe(df[COL["season"]].value_counts().rename("count").to_frame(), use_container_width=True)
with col2:
    st.write("Holiday distribution")
    st.dataframe(df[COL["holiday"]].value_counts().rename("count").to_frame(), use_container_width=True)

st.markdown("---")
st.subheader("Data Preview")
st.dataframe(df.head(30), use_container_width=True)

with st.expander("Column list"):
    st.write(list(df.columns))
