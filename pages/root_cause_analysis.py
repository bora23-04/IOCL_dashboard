import streamlit as st
import pandas as pd
from utils.preprocessing import load_data
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import apply_theme

st.title("🔍 Root Cause Analysis (RCA)")
apply_theme()
st.markdown("Identify variables responsible for process disturbances and production losses.")
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
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Average Yield",
        f"{filtered_df['Product_Yield'].mean():.2f}%"
    )

with col2:
    st.metric(
        "Disturbed Events",
        int(filtered_df["Is_Disturbed"].sum())
    )

with col3:
    st.metric(
        "Control Stability",
        f"{filtered_df['Control_Stability_Index'].mean():.2f}"
    )

with col4:
    st.metric(
        "Average Reactor Temp",
        f"{filtered_df['Reactor_Temperature'].mean():.2f} °C"
    )


st.subheader("Correlation Analysis")

cols = [
    "Product_Yield",
    "Conversion_Rate",
    "Reactor_Temperature",
    "Reactor_Pressure",
    "Catalyst_Activity",
    "Feed_Flow_Rate",
    "Energy_Consumption",
    "Control_Stability_Index"
]

corr = filtered_df[cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="Blues",
    title="Correlation Heatmap"
)

st.plotly_chart(fig, width="stretch")
left,right = st.columns(2)

with left:

    temp = filtered_df.groupby(
        "External_Disturbance_Type"
    )["Product_Yield"].mean().reset_index()

    fig = px.bar(
        temp,
        x="External_Disturbance_Type",
        y="Product_Yield",
        color="External_Disturbance_Type",
        color_discrete_sequence=px.colors.qualitative.Set3,
        title="Average Yield by Disturbance"
    )

    st.plotly_chart(fig,width="stretch")
with right:

    fig = px.scatter(
        filtered_df,
        x="Reactor_Temperature",
        y="Product_Yield",
        color="Yield_Category",
        trendline="ols",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Reactor Temperature vs Product Yield"
    )

    st.plotly_chart(fig,width="stretch")

left,right = st.columns(2)

features = [
    "Reactor_Temperature",
    "Reactor_Pressure",
    "Feed_Flow_Rate",
    "Catalyst_Activity",
    "Air_Flow_Rate",
    "Energy_Consumption",
    "Control_Stability_Index"
]

importance = []

for col in features:
    importance.append({
        "Feature":col,
        "Correlation":abs(filtered_df[col].corr(filtered_df["Product_Yield"]))
    })

importance = pd.DataFrame(importance)
importance = importance.sort_values("Correlation")
with left:

    fig = px.bar(
        importance,
        x="Correlation",
        y="Feature",
        orientation="h",
        color="Correlation",
        color_continuous_scale="Teal",
        title="Variables Influencing Product Yield"
    )

    st.plotly_chart(fig,width="stretch")
with right:

    fig = px.line(
        filtered_df,
        x="Timestamp",
        y="Control_Stability_Index",
        title="Control Stability Trend"
    )

    fig.update_traces(line_color="#90be6d")

    st.plotly_chart(fig,width="stretch")
    #
    # fig = px.histogram(
    #     filtered_df,
    #     x="External_Disturbance_Type",
    #     color="External_Disturbance_Type",
    #     color_discrete_sequence=px.colors.qualitative.Pastel,
    #     title="External Disturbance Distribution"
    # )
    #
    # st.plotly_chart(fig,use_container_width=True)
# -----------------------------------------
# SUMMARY
# -----------------------------------------
st.divider()

st.subheader("Root Cause Summary")

summary = importance.sort_values(
    "Correlation",
    ascending=False
)

st.dataframe(summary,width="stretch")
st.divider()

st.subheader("Analysis Insights")

top = summary.iloc[0]["Feature"]

st.success(f"""
• The strongest factor affecting Product Yield is **{top}**.

• External disturbances reduce average product yield.

• Reactor temperature variation directly impacts conversion.

• Lower Control Stability Index is associated with reduced process performance.

• These variables should be prioritized during process optimization.
""")
