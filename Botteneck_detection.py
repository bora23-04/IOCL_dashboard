import streamlit as st
import pandas as pd
from utils.preprocessing import load_data
import plotly.express as px
from utils.theme import apply_theme
st.title("🚧 Process Bottleneck Detection")
apply_theme()
st.markdown(
    """
Detect process bottlenecks by monitoring equipment utilization,
production efficiency and process variables.
"""
)

st.divider()
# -----------------------------
# Load Data
# -----------------------------
df = load_data()

# Convert Timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Dashboard Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["Timestamp"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["Timestamp"].max().date()
)

shift = st.sidebar.multiselect(
    "Shift",
    options=df["Shift"].unique(),
    default=df["Shift"].unique()
)

day = st.sidebar.multiselect(
    "Day",
    options=df["DayOfWeek"].unique(),
    default=df["DayOfWeek"].unique()
)

disturbance = st.sidebar.selectbox(
    "Disturbance Status",
    ["All", "Disturbed", "Normal"]
)

# -----------------------------
# Apply Filters
# -----------------------------
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
# -----------------------------
# KPI CARDS
# -----------------------------
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Average Yield",
        f"{filtered_df['Product_Yield'].mean():.2f}%"
    )

with col2:
    st.metric(
        "Average Conversion",
        f"{filtered_df['Conversion_Rate'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Average Energy",
        f"{filtered_df['Energy_Consumption'].mean():.2f}"
    )

with col4:
    st.metric(
        "Disturbed Periods",
        int(filtered_df["Is_Disturbed"].sum())
    )

st.divider()
# -----------------------------
# Reactor Temperature & Pressure
# -----------------------------
left,right = st.columns(2)

with left:

    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Reactor_Temperature",
        title="Reactor Temperature Trend"
    )

    fig.update_traces(line_color="#8ecae6")

    st.plotly_chart(fig,use_container_width=True)

with right:

    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Reactor_Pressure",
        title="Reactor Pressure Trend"
    )

    fig.update_traces(line_color="#90be6d")

    st.plotly_chart(fig,use_container_width=True)
# -----------------------------
# Feed Flow & Catalyst Activity
# -----------------------------
left,right = st.columns(2)

with left:

    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Feed_Flow_Rate",
        title="Feed Flow Rate"
    )

    fig.update_traces(line_color="#f9c74f")

    st.plotly_chart(fig,use_container_width=True)

with right:

    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Catalyst_Activity",
        title="Catalyst Activity"
    )
    fig.update_traces(line_color="#f4a261")

    st.plotly_chart(fig,use_container_width=True)

# -----------------------------
# Energy vs Product Yield
# -----------------------------
left,right = st.columns(2)

with left:

    fig = px.scatter(
        filtered_df,
        x="Energy_Consumption",
        y="Product_Yield",
        color="Yield_Category",
        trendline="ols",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Energy Consumption vs Product Yield"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    fig = px.scatter(
        filtered_df,
        x="Feed_Flow_Rate",
        y="Conversion_Rate",
        color="Shift",
        trendline="ols",
        color_discrete_sequence=px.colors.qualitative.Set3,
        title="Feed Flow vs Conversion"
    )

    st.plotly_chart(fig,use_container_width=True)
# -----------------------------
# Yield by Shift & Disturbances
# -----------------------------
left,right = st.columns(2)

with left:

    shift_df = filtered_df.groupby("Shift")["Product_Yield"].mean().reset_index()

    fig = px.bar(
        shift_df,
        x="Shift",
        y="Product_Yield",
        color="Shift",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Average Yield by Shift"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    disturb_df = filtered_df.groupby(
        "External_Disturbance_Type"
    )["Energy_Consumption"].mean().reset_index()

    fig = px.bar(
        disturb_df,
        x="External_Disturbance_Type",
        y="Energy_Consumption",
        color="External_Disturbance_Type",
        color_discrete_sequence=px.colors.qualitative.Set3,
        title="Energy Consumption by Disturbance"
    )

    st.plotly_chart(fig,use_container_width=True)
# -----------------------------
# Bottleneck Ranking
# -----------------------------
st.divider()

st.subheader("Potential Bottleneck Ranking")

bottleneck = pd.DataFrame({

    "Process Variable":[
        "Energy Consumption",
        "Reactor Temperature",
        "Feed Flow Rate",
        "Catalyst Activity",
        "Pressure"
    ],

    "Average Value":[
        filtered_df["Energy_Consumption"].mean(),
        filtered_df["Reactor_Temperature"].mean(),
        filtered_df["Feed_Flow_Rate"].mean(),
        filtered_df["Catalyst_Activity"].mean(),
        filtered_df["Reactor_Pressure"].mean()
    ]

})

fig = px.bar(

    bottleneck.sort_values("Average Value"),

    x="Average Value",

    y="Process Variable",

    orientation="h",

    color="Average Value",

    color_continuous_scale="Teal",

    title="Potential Bottleneck Ranking"

)

st.plotly_chart(fig,use_container_width=True)
# -----------------------------
# SUMMARY
# -----------------------------
st.divider()

st.subheader("Bottleneck Summary")

st.dataframe(bottleneck,use_container_width=True)
st.divider()

st.subheader("Process Insights")

highest = bottleneck.sort_values(
    "Average Value",
    ascending=False
).iloc[0]["Process Variable"]

st.success(f"""

### Observations

• **{highest}** shows the highest operating value and may represent the primary bottleneck.

• Higher energy consumption is associated with lower process efficiency.

• Catalyst activity directly impacts conversion and product yield.

• Feed flow fluctuations create unstable operating conditions.

• Reactor temperature deviations contribute to production losses.

• These variables should be continuously monitored to improve refinery throughput.

""")
