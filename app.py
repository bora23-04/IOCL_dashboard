import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.preprocessing import load_data
from utils.theme import apply_theme

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="IOCL Process Data Analytics",
    page_icon="🏭",
    layout="wide"
)
apply_theme()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = load_data()

# ---------------------------------------------------
# CONVERT TIMESTAMP
# ---------------------------------------------------
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

df = df.dropna(subset=["Timestamp"])

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("🏭 IOCL Process Data Analytics Platform")
st.markdown("### Executive Overview")
st.divider()

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("Dashboard Filters")

# Date Filter
start_date = st.sidebar.date_input(
    "Start Date",
    value=df["Timestamp"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["Timestamp"].max().date()
)

# Shift Filter
shift = st.sidebar.multiselect(
    "Shift",
    options=df["Shift"].unique(),
    default=df["Shift"].unique()
)

# Day Filter
day = st.sidebar.multiselect(
    "Day",
    options=df["DayOfWeek"].unique(),
    default=df["DayOfWeek"].unique()
)

# Disturbance Filter
disturbance = st.sidebar.selectbox(
    "Disturbance Status",
    ["All", "Disturbed", "Normal"]
)

# Date filtering
filtered_df = df[
    (df["Timestamp"].dt.date >= start_date) &
    (df["Timestamp"].dt.date <= end_date)
]

# Shift filtering
filtered_df = filtered_df[
    filtered_df["Shift"].isin(shift)
]

# Day filtering
filtered_df = filtered_df[
    filtered_df["DayOfWeek"].isin(day)
]

# Disturbance filtering
if disturbance == "Disturbed":
    filtered_df = filtered_df[
        filtered_df["Is_Disturbed"] == 1
    ]

elif disturbance == "Normal":
    filtered_df = filtered_df[
        filtered_df["Is_Disturbed"] == 0
    ]

yield_category = st.sidebar.multiselect(
    "Yield Category",
    options=df["Yield_Category"].unique(),
    default=df["Yield_Category"].unique()
)

feed_change = st.sidebar.multiselect(
    "Feed Change Event",
    options=df["Feed_Change_Event"].unique(),
    default=df["Feed_Change_Event"].unique()
)

catalyst = st.sidebar.multiselect(
    "Catalyst Replacement",
    options=df["Catalyst_Replacement"].unique(),
    default=df["Catalyst_Replacement"].unique()
)
filtered_df = filtered_df[
    filtered_df["Yield_Category"].isin(yield_category)
]

filtered_df = filtered_df[
    filtered_df["Feed_Change_Event"].isin(feed_change)
]

filtered_df = filtered_df[
    filtered_df["Catalyst_Replacement"].isin(catalyst)
]
# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Product Yield",
        f"{filtered_df['Product_Yield'].mean():.2f}%"
    )

with col2:
    st.metric(
        "Average Conversion",
        f"{filtered_df['Conversion_Rate'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Average Reactor Temp",
        f"{filtered_df['Reactor_Temperature'].mean():.1f} °C"
    )

with col4:
    st.metric(
        "Average Pressure",
        f"{filtered_df['Reactor_Pressure'].mean():.2f} bar"
    )

st.divider()

health_score = filtered_df["Control_Stability_Index"].mean()

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=health_score,
    title={"text": "Overall Process Health"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "#3498DB"},
        "bgcolor": "white",
        "borderwidth": 2,
        "bordercolor": "#D6DBDF",
        "steps": [
            {"range": [0, 40], "color": "#F1948A"},
            {"range": [40, 70], "color": "#F7DC6F"},
            {"range": [70, 100], "color": "#82E0AA"}
        ]
    }
))

st.plotly_chart(fig, width="stretch")
# ---------------------------------------------------
# SECOND KPI ROW
# ---------------------------------------------------

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Energy Consumption",
        f"{filtered_df['Energy_Consumption'].mean():.2f}"
    )

with col6:
    st.metric(
        "NOx Emissions",
        f"{filtered_df['Emissions_NOx'].mean():.2f}"
    )

with col7:
    st.metric(
        "SOx Emissions",
        f"{filtered_df['Emissions_SOx'].mean():.2f}"
    )

with col8:
    st.metric(
        "Control Stability",
        f"{filtered_df['Control_Stability_Index'].mean():.2f}"
    )

st.divider()

# ==========================================================
# ROW 1
# ==========================================================

left,right = st.columns(2)

with left:

    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Product_Yield",
        title="Product Yield Trend"
    )
    fig.update_traces(line_color="#8ecae6")

    st.plotly_chart(fig, width="stretch")

with right:

    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Conversion_Rate",
        title="Conversion Rate Trend"
    )
    fig.update_traces(line_color="#90be6d")
    st.plotly_chart(fig, width="stretch")

# ==========================================================
# ROW 2
# ==========================================================

left,right = st.columns(2)

with left:

    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Reactor_Temperature",
        title="Reactor Temperature"
    )
    fig.update_traces(line_color="#f9c74f")

    st.plotly_chart(fig, width="stretch")

with right:

    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Reactor_Pressure",
        title="Reactor Pressure"
    )
    fig.update_traces(line_color="#f4a261")
    st.plotly_chart(fig, width="stretch")

# ==========================================================
# ROW 3
# ==========================================================

left,right = st.columns(2)

with left:

    fig = px.histogram(
        filtered_df,
        x="Yield_Category",
        color="Yield_Category",
        title="Yield Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    st.plotly_chart(fig, width="stretch")

with right:

    fig = px.bar(
        filtered_df.groupby("Shift")["Product_Yield"].mean().reset_index(),
        x="Shift",
        y="Product_Yield",
        color="Shift",
        title="Average Yield by Shift",
        color_discrete_sequence = px.colors.qualitative.Set3
    )

    st.plotly_chart(fig, width="stretch")

st.divider()

disturbed = filtered_df["Is_Disturbed"].sum()


yield_avg = filtered_df["Product_Yield"].mean()
conversion = filtered_df["Conversion_Rate"].mean()
pressure = filtered_df["Reactor_Pressure"].mean()

summary = f"""

### Current Refinery Status

- Average Product Yield : **{yield_avg:.2f}%**

- Average Conversion Rate : **{conversion:.2f}%**

- Average Reactor Pressure : **{pressure:.2f} bar**

- Disturbed Events : **{disturbed}**

The refinery is currently operating under the selected filter conditions.

This dashboard provides a high-level overview before moving to detailed Root Cause Analysis, Bottleneck Detection and Six Sigma Analysis.
"""

st.markdown(summary)

st.subheader("Recent Process Data")

st.dataframe(filtered_df.tail(20),width="stretch")