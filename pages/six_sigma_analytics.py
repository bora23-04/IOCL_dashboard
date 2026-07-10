import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import norm
import numpy as np
from utils.theme import apply_theme
from utils.preprocessing import load_data

st.set_page_config(page_title="Six Sigma Analytics", layout="wide")

df = load_data()

df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

st.title("📊 Six Sigma Analytics")
apply_theme()
st.markdown("Statistical Process Control and Process Capability Analysis")
st.divider()

# -----------------------------
# Filters
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

target = st.sidebar.selectbox(
    "Process Variable",
    [
        "Product_Yield",
        "Conversion_Rate",
        "Reactor_Temperature",
        "Reactor_Pressure",
        "Energy_Consumption"
    ]
)

filtered = df[
    (df["Shift"].isin(shift)) &
    (df["DayOfWeek"].isin(day))
]
# -----------------------------
# KPI
# -----------------------------
mean = filtered[target].mean()
std = filtered[target].std()

USL = mean + 3 * std
LSL = mean - 3 * std

Cp = (USL - LSL) / (6 * std)

Cpu = (USL - mean) / (3 * std)
Cpl = (mean - LSL) / (3 * std)

Cpk = min(Cpu, Cpl)

Sigma = 3 * Cpk + 1.5

col1,col2,col3,col4 = st.columns(4)

col1.metric("Mean",f"{mean:.2f}")

col2.metric("Std Deviation",f"{std:.2f}")

col3.metric("Cp",f"{Cp:.2f}")

col4.metric("Cpk",f"{Cpk:.2f}")

# -----------------------------
# KPI II
# -----------------------------
st.divider()
col1,col2,col3,col4 = st.columns(4)

col1.metric("Sigma Level",f"{Sigma:.2f}")

outside = filtered[
    (filtered[target] > USL) |
    (filtered[target] < LSL)
]

col2.metric("Defects",len(outside))

defect_rate = len(outside)/len(filtered)*100

col3.metric("Defect Rate",f"{defect_rate:.2f}%")

yield_percent = 100-defect_rate

col4.metric("Process Yield",f"{yield_percent:.2f}%")

st.divider()
#--------------------------
#Sigma Level Status
#---------------------------
col1,col2,col3,col4 = st.columns(4)

col1.metric("Sigma Level",f"{Sigma:.2f}")

outside = filtered[
    (filtered[target] > USL) |
    (filtered[target] < LSL)
]

col2.metric("Defects",len(outside))

defect_rate = len(outside)/len(filtered)*100

col3.metric("Defect Rate",f"{defect_rate:.2f}%")

yield_percent = 100-defect_rate

col4.metric("Process Yield",f"{yield_percent:.2f}%")
if Sigma >= 6:
    st.success(f"Current Sigma Level : {Sigma:.2f} (World-Class Process)")

elif Sigma >= 4:
    st.warning(f"Current Sigma Level : {Sigma:.2f} (Good but Can Improve)")

else:
    st.error(f"Current Sigma Level : {Sigma:.2f} (Process Needs Improvement)")
# -----------------------------
# Capability Interpretation
# -----------------------------
st.subheader("Process Capability Interpretation")

if Cpk >= 1.33:
    st.success("Excellent Process Capability (Cpk > 1.33)")

elif Cpk >= 1:
    st.warning("Process is Acceptable but Needs Improvement")

else:
    st.error("Process is Not Capable. Root Cause Investigation Required.")
# -----------------------------
# Control Chart + Histogram
# -----------------------------
left,right = st.columns(2)

with left:

    fig = px.line(
        filtered,
        x="Timestamp",
        y=target,
        title="Control Chart",
        color_discrete_sequence=["#5DADE2"]
    )

    fig.add_hline(y=USL,line_dash="dash",line_color="red")
    fig.add_hline(y=LSL,line_dash="dash",line_color="red")
    fig.add_hline(y=mean,line_dash="dot",line_color="green")

    st.plotly_chart(fig,width="stretch")

with right:

    fig = px.histogram(
        filtered,
        x=target,
        nbins=25,
        title="Process Distribution",
        color_discrete_sequence=["#AED6F1"]
    )

    st.plotly_chart(fig,width="stretch")
st.subheader("SPC Rules")

if len(outside)==0:
    st.success("✔ Process is statistically under control.")
else:
    st.error(f"⚠ {len(outside)} observations are outside specification limits.")
# -----------------------------
# Box Plot + Scatter Plot
# -----------------------------
left,right = st.columns(2)

with left:

    fig = px.box(
        filtered,
        y=target,
        title="Variation Analysis",
        color_discrete_sequence=["#A9DFBF"]
    )

    st.plotly_chart(fig,width="stretch")

with right:

    fig = px.scatter(
        filtered,
        x="Timestamp",
        y=target,
        color="Shift",
        title="Scatter Plot",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    st.plotly_chart(fig,width="stretch")
# -----------------------------
# DEFECT ANALYSIS
# -----------------------------
left,right = st.columns(2)

with left:

    defects = pd.DataFrame({
        "Status":["Within Limit","Outside Limit"],
        "Count":[
            len(filtered)-len(outside),
            len(outside)
        ]
    })

    fig = px.pie(
        defects,
        names="Status",
        values="Count",
        title="Defect Distribution",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    st.plotly_chart(fig,width="stretch")

with right:

    fig = px.bar(
        filtered.groupby("Shift")[target].mean().reset_index(),
        x="Shift",
        y=target,
        color="Shift",
        title="Average Process by Shift",
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    st.plotly_chart(fig,width="stretch")
csv = filtered.to_csv(index=False)

st.download_button(
    " Download Six Sigma Report",
    csv,
    "SixSigmaReport.csv",
    "text/csv"
)
st.subheader("Recommendations")

if Cpk < 1:
    st.error("""
• Investigate process variation

• Perform Root Cause Analysis

• Tune PID Controller

• Improve Feed Quality

• Reduce Disturbances
""")

elif Cpk < 1.33:
    st.warning("""
• Process is acceptable

• Monitor continuously

• Reduce variation
""")

else:
    st.success("""
• Excellent Process Capability

• Maintain current operating conditions

• Continue SPC Monitoring
""")
st.divider()

st.caption("""
Industrial Process Monitoring Dashboard

Module : Six Sigma Analytics

Purpose : Statistical Process Control, Process Capability Analysis, and Defect Detection
""")