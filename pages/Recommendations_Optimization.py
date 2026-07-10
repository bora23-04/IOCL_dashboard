import streamlit as st
import pandas as pd
import plotly.express as px
from utils.preprocessing import load_data
from utils.theme import apply_theme
st.set_page_config(
    page_title="Recommendations & Optimization",
    layout="wide"
)
apply_theme()
df = load_data()

df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

st.title("🎯 Recommendations & Optimization")

st.markdown("AI-driven recommendations for improving refinery performance.")

st.divider()
# -----------------------------
# FILTERS
# -----------------------------
st.sidebar.header("Filters")

shift = st.sidebar.multiselect(
    "Shift",
    df["Shift"].unique(),
    default=df["Shift"].unique()
)

day = st.sidebar.multiselect(
    "Day",
    df["DayOfWeek"].unique(),
    default=df["DayOfWeek"].unique()
)

filtered = df[
    (df["Shift"].isin(shift)) &
    (df["DayOfWeek"].isin(day))
]
# -----------------------------
# KPI
# -----------------------------
yield_avg = filtered["Product_Yield"].mean()

conversion = filtered["Conversion_Rate"].mean()

energy = filtered["Energy_Consumption"].mean()

nox = filtered["Emissions_NOx"].mean()

stability = filtered["Control_Stability_Index"].mean()

disturbed = filtered["Is_Disturbed"].sum()
col1,col2,col3,col4,col5 = st.columns(5)

col1.metric("Yield",f"{yield_avg:.2f}%")

col2.metric("Conversion",f"{conversion:.2f}%")

col3.metric("Energy",f"{energy:.2f}")

col4.metric("NOx",f"{nox:.2f}")

col5.metric("Disturbances",disturbed)

st.divider()
# -----------------------------
# CHARTS
# -----------------------------
left,right = st.columns(2)

with left:

    recommendation = pd.DataFrame({

        "Area":[
            "Yield",
            "Conversion",
            "Energy",
            "Emissions",
            "Stability"
        ],

        "Score":[
            yield_avg,
            conversion,
            100-energy,
            100-nox,
            stability
        ]

    })

    fig = px.bar(

        recommendation,

        x="Area",

        y="Score",

        color="Area",

        title="Overall Performance",

        color_discrete_sequence=px.colors.qualitative.Pastel

    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    fig = px.pie(

        names=["Normal","Disturbed"],

        values=[
            len(filtered)-disturbed,
            disturbed
        ],

        title="Operating Condition",

        color_discrete_sequence=px.colors.qualitative.Set3

    )

    st.plotly_chart(fig,use_container_width=True)
#------------------------
#PRIORITY CHARTS
#------------------------
priority = pd.DataFrame({

    "Priority":[
        "Control Stability",
        "Energy Reduction",
        "Yield Improvement",
        "Emission Reduction",
        "Catalyst Health"
    ],

    "Importance":[95,90,88,84,80]

})

fig = px.bar(

    priority,

    x="Importance",

    y="Priority",

    orientation="h",

    color="Importance",

    title="Optimization Priority",

    color_continuous_scale="Blues"

)

st.plotly_chart(fig,use_container_width=True)
#-------------------------
#Recommendation
#-------------------------
st.subheader("AI Recommendations")

if stability < 80:

    st.error("""
 Improve PID tuning to reduce process instability.
""")

else:

    st.success("""
 Process stability is satisfactory.
""")

if yield_avg < 75:

    st.warning("""
 Optimize Catalyst-to-Oil Ratio to improve product yield.
""")

if energy > df["Energy_Consumption"].mean():

    st.warning("""
 Reduce energy consumption by improving reactor efficiency.
""")

if nox > df["Emissions_NOx"].mean():

    st.warning("""
 Optimize air flow to reduce NOx emissions.
""")

if disturbed > len(filtered)*0.10:

    st.error("""
 High disturbance frequency detected.
Investigate feedstock quality and external disturbances.
""")
#----------------------------
#Action Plan
#----------------------------
st.subheader("Optimization Action Plan")

actions = pd.DataFrame({

    "Issue":[
        "Low Yield",
        "High Energy",
        "High NOx",
        "Poor Stability",
        "Frequent Disturbances"
    ],

    "Recommended Action":[
        "Optimize Catalyst/Oil Ratio",
        "Improve Heat Integration",
        "Optimize Air Flow",
        "Retune PID Controller",
        "Improve Feed Quality"
    ],

    "Expected Benefit":[
        "+4% Yield",
        "-6% Energy",
        "-8% NOx",
        "+15 Stability",
        "-30% Disturbances"
    ]

})

st.dataframe(actions,use_container_width=True)
#----------------------
#SUMMARY
#----------------------
st.subheader("Executive Recommendation")

summary = f"""

### Overall Assessment

• Average Product Yield : **{yield_avg:.2f}%**

• Average Conversion Rate : **{conversion:.2f}%**

• Average Energy Consumption : **{energy:.2f}**

• Average NOx Emission : **{nox:.2f}**

• Process Stability Index : **{stability:.2f}**

### Recommended Actions

• Optimize Catalyst-to-Oil Ratio

• Improve PID Controller Tuning

• Reduce Energy Consumption

• Monitor Reactor Temperature Continuously

• Reduce Feedstock Disturbances

• Implement Predictive Maintenance

**Expected Benefits**

• Higher Product Yield

• Lower Energy Consumption

• Reduced Emissions

• Improved Process Stability

• Better Overall Refinery Efficiency

"""

st.markdown(summary)
#--------------------
#DOWNLOAD REPORT
#--------------------
csv = actions.to_csv(index=False)

st.download_button(

    "Download Optimization Report",

    csv,

    file_name="Optimization_Report.csv",

    mime="text/csv"

)