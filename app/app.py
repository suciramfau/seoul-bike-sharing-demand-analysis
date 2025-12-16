import streamlit as st
from utils import (
    load_data,
    harmonize_columns,
    standardize_types,
    filter_functioning_days,
    add_time_features,
    COL,
)

st.set_page_config(
    page_title="Seoul Bike Sharing Demand",
    page_icon="🚲",
    layout="wide",
)

st.title("🚲 Seoul Bike Sharing Demand Analysis")
st.caption(
    "Portfolio analytics app: time patterns, weekday vs holiday behavior, weather/season effects, "
    "and actionable recommendations for operations & promotions."
)

# Global sidebar controls (shared through session_state)
st.sidebar.header("Data Settings")
default_path = st.session_state.get("data_path", "data/seoulbike_cleaned.csv")
default_filter = st.session_state.get("apply_filter", True)

data_path = st.sidebar.text_input("Dataset path", value=default_path, key="data_path")
apply_filter = st.sidebar.checkbox("Filter Functioning Day == Yes", value=default_filter, key="apply_filter")

# Load & prepare once for the landing KPIs (pages will reload on their own too)
df = load_data(data_path)
df = harmonize_columns(df)
df = standardize_types(df)
if apply_filter:
    df = filter_functioning_days(df)
df = add_time_features(df)

# KPI cards
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{df.shape[0]:,}")
c2.metric("Columns", f"{df.shape[1]:,}")

if COL["target"] in df.columns:
    c3.metric("Total Rentals", f"{int(df[COL['target']].sum()):,}")
    c4.metric("Avg Hourly Rentals", f"{df[COL['target']].mean():.0f}")
else:
    c3.metric("Total Rentals", "N/A")
    c4.metric("Avg Hourly Rentals", "N/A")
    st.warning(
        f"Target column not found. Expected: '{COL['target']}'. "
        "Go to Overview → Column list to inspect detected columns."
    )

st.markdown("---")

st.subheader("Business Problem")
st.write(
    """
    How can bike-sharing operators optimize bike availability and promotional strategies
    based on differences in usage patterns between weekdays and holidays, as well as the impact
    of weather and seasonal conditions?
    """
)

st.subheader("How to use this app")
st.write(
    """
    Navigate using the pages in the left sidebar:
    - **Overview**: dataset snapshot & KPIs
    - **Demand Patterns**: peak hour analysis
    - **Weekday vs Holiday**: behavioral differences
    - **Weather & Season**: external factors
    - **Recommendations**: actionable operations playbook
    """
)

with st.expander("Data preview"):
    st.dataframe(df.head(25), use_container_width=True)

st.info(
    "All charts and insights in this app are generated from the **cleaned dataset** (`seoulbike_cleaned.csv`). "
    "Power BI is treated as a visualization layer and does not require a separate dataset in this repository."
)
