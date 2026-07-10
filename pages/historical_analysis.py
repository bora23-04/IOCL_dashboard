import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import apply_theme
from utils.preprocessing import load_data

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------
st.set_page_config(
    page_title="Historical Analysis",
    page_icon="📈",
    layout="wide"
)
apply_theme()
# -----------------------------------------
# LOAD DATA
# -----------------------------------------
df = load_data()

# -----------------------------------------
# CONVERT TIMESTAMP
# -----------------------------------------
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

df = df.dropna(subset=["Timestamp"])

# -----------------------------------------
# PAGE TITLE
# -----------------------------------------
st.title("📈 Historical Process Analysis")
st.markdown("### Long-Term Performance Analysis")
st.divider()

# -----------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------
st.sidebar.header("Dashboard Filters")

# Date Range
start_date = st.sidebar.date_input(
    "Start Date",
    value=df["Timestamp"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["Timestamp"].max().date()
)

# Shift
shift = st.sidebar.multiselect(
    "Shift",
    options=sorted(df["Shift"].dropna().unique()),
    default=sorted(df["Shift"].dropna().unique())
)

# Day
day = st.sidebar.multiselect(
    "Day",
    options=sorted(df["DayOfWeek"].dropna().unique()),
    default=sorted(df["DayOfWeek"].dropna().unique())
)

# Disturbance
disturbance = st.sidebar.selectbox(
    "Disturbance Status",
    ["All", "Disturbed", "Normal"]
)

# -----------------------------------------
# APPLY FILTERS
# -----------------------------------------
filtered_df = df[
    (df["Timestamp"].dt.date >= start_date) &
    (df["Timestamp"].dt.date <= end_date)
]

filtered_df = filtered_df[
    filtered_df["Shift"].isin(shift)
]

filtered_df = filtered_df[
    filtered_df["DayOfWeek"].isin(day)
]

if disturbance == "Disturbed":
    filtered_df = filtered_df[
        filtered_df["Is_Disturbed"] == 1
    ]

elif disturbance == "Normal":
    filtered_df = filtered_df[
        filtered_df["Is_Disturbed"] == 0
    ]

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

# st.divider()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Maximum Product Yield",
        f"{filtered_df['Product_Yield'].max():.2f}%"
    )

with col2:
    st.metric(
        "Minimum Product Yield",
        f"{filtered_df['Product_Yield'].min():.2f}%"
    )

with col3:
    st.metric(
        "Maximum Reactor Temperature",
        f"{filtered_df['Reactor_Temperature'].max():.2f} °C"
    )

with col4:
    st.metric(
        "Average Energy Consumption",
        f"{filtered_df['Energy_Consumption'].mean():.2f}"
    )
# ==========================================================
# KPI CARDS
# ==========================================================
st.divider()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Product Yield",
        f"{filtered_df['Product_Yield'].mean():.2f}%"
    )

with col2:
    st.metric(
        "Maximum Yield",
        f"{filtered_df['Product_Yield'].max():.2f}%"
    )

with col3:
    st.metric(
        "Minimum Yield",
        f"{filtered_df['Product_Yield'].min():.2f}%"
    )

with col4:
    st.metric(
        "Average Conversion Rate",
        f"{filtered_df['Conversion_Rate'].mean():.2f}%"
    )

st.divider()

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Average Reactor Temperature",
        f"{filtered_df['Reactor_Temperature'].mean():.2f} °C"
    )

with col6:
    st.metric(
        "Maximum Reactor Temperature",
        f"{filtered_df['Reactor_Temperature'].max():.2f} °C"
    )

with col7:
    st.metric(
        "Average Energy Consumption",
        f"{filtered_df['Energy_Consumption'].mean():.2f}"
    )

with col8:
    st.metric(
        "Average Control Stability",
        f"{filtered_df['Control_Stability_Index'].mean():.2f}"
    )

st.divider()
# ==========================================================
# CHARTS
# ==========================================================

st.subheader("Historical Trends")

col1, col2 = st.columns(2)

with col1:
    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Product_Yield",
        title="Product Yield Over Time",
        # color_discrete_sequence=["blue"]
    )
    fig.update_traces(line_color="#8ecae6")
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Yield (%)"
    )

    st.plotly_chart(fig,width="stretch")

with col2:
    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Conversion_Rate",
        title="Conversion Rate Over Time",
        # color_discrete_sequence=["green"]
    )
    fig.update_traces(line_color="#90be6d")
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Conversion (%)"
    )

    st.plotly_chart(fig, width="stretch")
col1, col2 = st.columns(2)

with col1:
    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Energy_Consumption",
        title="Energy Consumption Trend",
        # color_discrete_sequence=["red"]
    )
    fig.update_traces(line_color="#f9c74f")
    st.plotly_chart(fig, width="stretch")

with col2:
    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Control_Stability_Index",
        title="Control Stability Trend",
        # color_discrete_sequence=["purple"]
    )
    fig.update_traces(line_color="#f4a261")
    st.plotly_chart(fig, width="stretch")

# ==========================================================
# Monthly / Shift-wise Analysis
# ==========================================================
st.divider()

st.subheader("Performance Comparison")

col1, col2 = st.columns(2)
with col1:

    shift_avg = (
        filtered_df.groupby("Shift")[[
            "Product_Yield",
            "Conversion_Rate"
        ]]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        shift_avg,
        x="Shift",
        y=["Product_Yield", "Conversion_Rate"],
        barmode="group",
        title="Shift-wise Performance"
    )

    st.plotly_chart(fig, width="stretch")
with col2:

    day_avg = (
        filtered_df.groupby("DayOfWeek")[
            "Product_Yield"
        ]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        day_avg,
        x="DayOfWeek",
        y="Product_Yield",
        color="DayOfWeek",
        title="Average Yield by Day"
    )

    st.plotly_chart(fig, width="stretch")
# ==========================================================
# Distribution Analysis
# ==========================================================
st.divider()

st.subheader("Distribution Analysis")

left, right = st.columns(2)
with left:

    fig = px.histogram(
        filtered_df,
        x="Product_Yield",
        nbins=20,
        color="Yield_Category",
        title="Product Yield Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig.update_layout(
        xaxis_title="Product Yield (%)",
        yaxis_title="Frequency"
    )

    st.plotly_chart(fig, width="stretch")
with right:

    fig = px.histogram(
        filtered_df,
        x="Conversion_Rate",
        nbins=20,
        color_discrete_sequence=["orange"],
        title="Conversion Rate Distribution"
    )

    fig.update_layout(
        xaxis_title="Conversion Rate (%)",
        yaxis_title="Frequency"
    )

    st.plotly_chart(fig, width="stretch")
# ==========================================================
# Distribution Analysis
# ==========================================================
st.divider()

st.subheader("Relationship Analysis")

left, right = st.columns(2)
with left:

    fig = px.scatter(
        filtered_df,
        x="Reactor_Temperature",
        y="Product_Yield",
        color="Shift",
        title="Reactor Temperature vs Product Yield"
       
    )

    fig.update_layout(
        xaxis_title="Reactor Temperature (°C)",
        yaxis_title="Product Yield (%)"
    )

    st.plotly_chart(fig, width="stretch")
with right:

    fig = px.scatter(
        filtered_df,
        x="Catalyst_Activity",
        y="Conversion_Rate",
        color="Shift",
        title="Catalyst Activity vs Conversion Rate"
        
    )

    fig.update_layout(
        xaxis_title="Catalyst Activity",
        yaxis_title="Conversion Rate (%)"
    )

    st.plotly_chart(fig, width="stretch")
