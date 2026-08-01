import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Junction Box Weight Calculator", layout="wide")

st.title("🧮 Junction Box Weight Calculator")
st.markdown("Calculate the material weight of a 6-sided junction box based on its dimensions, thickness, and material.")

st.divider()

# --- Input Section ---
st.subheader("1. Enter Specifications")

# Material Dropdown
material = st.selectbox("Select Material", ["Stainless Steel", "Mild Steel"])

# Set SG internally based on material selection
if material == "Stainless Steel":
    sg = 7.95
else:
    sg = 7.85

st.write("---") 

# Inputs across 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    L = st.number_input("Length (L) in mm", value=300.0, step=10.0)
    thickness = st.number_input("Thickness in mm", value=2.0, step=0.5)

with col2:
    W = st.number_input("Width (W) in mm", value=300.0, step=10.0)
    wastage = st.number_input("Wastage Percentage (%)", value=10.0, step=1.0)

with col3:
    H = st.number_input("Height (H) in mm", value=160.0, step=10.0)


# --- Dynamic 3D Visualization ---
st.divider()
st.subheader("2. Dynamic Box Visualization")

def create_3d_box(l, w, h):
    # Tracing the 12 edges of the 3D box to create a wireframe
    x = [0, l, l, 0, 0, 0, l, l, 0, 0, l, l, l, l, 0, 0]
    y = [0, 0, w, w, 0, 0, 0, w, w, 0, 0, 0, w, w, w, w]
    z = [0, 0, 0, 0, 0, h, h, h, h, h, h, 0, 0, h, h, 0]

    fig = go.Figure(data=go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color='#1f77b4', width=5),
        hoverinfo='none'
    ))

    # Adding dimension labels (L, W, H) exactly like your sketch
    fig.add_trace(go.Scatter3d(
        x=[l/2, l, 0], 
        y=[0, w/2, 0], 
        z=[0, 0, h/2],
        mode='text',
        text=[f'L: {l}mm', f'W: {w}mm', f'H: {h}mm'],
        textposition=['bottom center', 'bottom center', 'middle left'],
        textfont=dict(size=14, color='red'),
        hoverinfo='none'
    ))

    # Setting aspectmode to 'data' forces the plot to physically stretch 
    # and match the actual L, W, H ratios provided by the user.
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Length', showticklabels=False),
            yaxis=dict(title='Width', showticklabels=False),
            zaxis=dict(title='Height', showticklabels=False),
            aspectmode='data' 
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False,
        height=450
    )
    return fig

# Display the interactive Plotly chart
st.plotly_chart(create_3d_box(L, W, H), use_container_width=True)


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
st.subheader("3. Side-by-Side Breakdown")

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
st.subheader("4. Final Weight Estimations")

# Display results in prominent metric cards
metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.metric(label="Total Bare Weight", value=f"{total_bare_weight:.4f} kg")

with metric_col2:
    st.metric(label=f"Final Weight (incl. {wastage}% Wastage)", value=f"{final_weight:.4f} kg")
