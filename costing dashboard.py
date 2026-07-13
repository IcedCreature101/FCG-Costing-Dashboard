import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Junction Box Weight Calculator", layout="wide")

st.title("🧮 Junction Box Weight Calculator")
st.markdown("Calculate the material weight of a 6-sided junction box based on its dimensions, thickness, and material.")

st.divider()

# --- Input Section ---
st.subheader("1. Enter Specifications")

# Material Dropdown
material = st.selectbox("Select Material", ["Stainless Steel", "Mild Steel"])

# Set SG internally based on material selection (No longer visible on screen)
if material == "Stainless Steel":
    sg = 7.95
else:
    sg = 7.85

st.write("---") 

# Rebalanced to fit 5 inputs across 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    L = st.number_input("Length (L) in mm", value=300.0, step=10.0)
    thickness = st.number_input("Thickness in mm", value=2.0, step=0.5)

with col2:
    W = st.number_input("Width (W) in mm", value=300.0, step=10.0)
    wastage = st.number_input("Wastage Percentage (%)", value=10.0, step=1.0)

with col3:
    H = st.number_input("Height (H) in mm", value=160.0, step=10.0)

# --- Calculation Logic ---
# 1. Calculate Areas
areas = {
    "Front Side (L x W)": L * W,
    "Back Side (L x W)": L * W,
    "Side - 1 (W x H)": W * H,
    "Side - 2 (W x H)": W * H,
    "Gland Plate - 1 (L x H)": L * H,
    "Gland Plate - 2 (L x H)": L * H
}

# 2. Build Data for the Table
data = []
for side_name, area in areas.items():
    volume = area * thickness
    weight = (volume * sg) / 1_000_000  # Convert mm^3 to kg
    data.append({
        "Side Name": side_name,
        "Area (mm²)": area,
        "Volume (mm³)": volume,
        "Weight (kg)": weight
    })

df = pd.DataFrame(data)

# --- Output Section ---
st.divider()
st.subheader("2. Side-by-Side Breakdown")

# Display the dataframe with formatted numbers
st.dataframe(
    df.style.format({
        "Area (mm²)": "{:,.2f}", 
        "Volume (mm³)": "{:,.2f}", 
        "Weight (kg)": "{:,.4f}"
    }),
    width='stretch'
)

# 3. Calculate Totals
total_bare_weight = df["Weight (kg)"].sum()
final_weight = total_bare_weight * (1 + (wastage / 100))

st.divider()
st.subheader("3. Final Weight Estimations")

# Display results in prominent metric cards
metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.metric(label="Total Bare Weight", value=f"{total_bare_weight:.4f} kg")

with metric_col2:
    st.metric(label=f"Final Weight (incl. {wastage}% Wastage)", value=f"{final_weight:.4f} kg")