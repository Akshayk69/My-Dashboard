import streamlit as st
import numpy as np
from matplotlib import pyplot as plt

## Sliders
st.title("Total Buy with Lifespan Adjustment")
# Sidebar: Control Panel
st.sidebar.header("Control Panel")
# 3. Product lifespan (weeks)
lifespan = st.sidebar.slider("Product Lifespan (weeks)", 4, 16, 12, 1)
# 4. Number of stores
stores = st.sidebar.slider("Number of Stores", 1, 50, 10, 1)

# 5. Generate realistic ROS data for 5 products
np.random.seed(2025)
raw_ros_data = np.array([
    [0.2, 0.5, 0.4, 0.2],
    [0.3, 0.6, 0.45, 0.25],
    [0.25, 0.55, 0.5, 0.3],
    [0.22, 0.52, 0.42, 0.2],
    [0.28, 0.58, 0.48, 0.25],
])

# Lifespan of similar products
similar_lifespans = np.array([10, 12, 12, 16, 10])
phases = ['Intro', 'Growth', 'Maturity', 'Decline']
# Adjust ROS to user-defined lifespan
ros_data = np.copy(raw_ros_data)

# Adjust only the decline phase (4th column, index 3)
ros_data[:, 3] = raw_ros_data[:, 3] * (lifespan / similar_lifespans)
ros_data[:, 3] = np.clip(ros_data[:, 3], 0, ros_data[:,0])    ## try with both, i.e growth and maturity

# 7. Compute avg ROS per phase
ros_mean = ros_data.mean(axis=0)

avg_ros_value = ros_mean.flatten().mean()
# 8. Compute total buy
total_buy_total = avg_ros_value * lifespan * stores

# Phase midpoints
stages = np.array([0.125, 0.375, 0.625, 0.875])

# Plot
fig, ax = plt.subplots(figsize=(6, 4))
# Connect new product's phase-wise ROS points
ax.plot(stages, ros_mean, 'k-o', label='PLM', linewidth=2.5, markersize=6)
ax2 = ax.twinx()
# ax2.plot( stores, 'g--o', lw=2, label='Stores')
# Vertical quarter lines at 25%, 50%, 75%
quarter_marks = [0.25, 0.5, 0.75]
for q in quarter_marks:
    ax.axvline(x=q, color='gray', linestyle='--', linewidth=1, alpha=0.6)
x_positions = [0.125, 0.375, 0.625, 0.875]  # Midpoints of each phase
for i, x in enumerate(x_positions):
    ax.text(x, ax.get_ylim()[0] - 0.02, phases[i],
            ha='center', va='top', fontsize=9, color='gray')
ax.hlines(y=avg_ros_value, xmin=0.0, xmax=1.0, colors='red', linestyles='--', linewidth=2, label=f"Avg.ROS = {avg_ros_value}")
# Formatting
ax.set_ylim(0, max(ros_mean.max() * 0.5, 1.0))
ax2.set_ylim(0, stores * 1.1)
ax.set_xlabel("Lifecycle (Normalized)")
ax.set_ylabel("ROS (per week)")
ax2.set_ylabel(" Store count")
ax.set_title("ROS for Total Buy ")
# ax.grid(alpha=0.2)
# Legends
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines + lines2, labels + labels2, loc='upper right')
st.pyplot(fig)


# Sidebar Summary (Concise)
st.sidebar.subheader("📊 Model Summary")
st.sidebar.markdown(f"""
- **Lifespan:** {lifespan} weeks  
- **Stores:** {stores}  
- **PLM ROS:** {avg_ros_value} 
- **Total Buy:** {int(total_buy_total)} units
""")

# -----------------------------------------
# 📊 Unified ROS Curve Plot: Similar Products + New Product
# -----------------------------------------
fig5, ax5 = plt.subplots(figsize=(6, 4))
colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728', '#9467bd']
# Plot 5 similar product ROS curves (interpolated)
for i in range(5):
    ros_i = raw_ros_data[i]
    curve_x = np.linspace(0, 1, 500)
    curve_y = np.interp(curve_x, stages, ros_i)
    ax5.plot(curve_x, curve_y, label=f"Product {i+1}, LS {similar_lifespans[i]}", color=colors[i], linewidth=1.8, alpha=0.7)
# Connect new product's phase-wise ROS points
ax5.plot(stages, ros_mean, 'k-o', label=f"PLM, LS {lifespan}", linewidth=2.5, markersize=6)
for q in quarter_marks:
    ax5.axvline(x=q, color='gray', linestyle='--', linewidth=1, alpha=0.6)
for i, x in enumerate(x_positions):
    ax5.text(x, ax5.get_ylim()[0] - 0.02, phases[i],
            ha='center', va='top', fontsize=9, color='gray')
# Formatting
ax5.set_title("Lifecycle ROS Comparison: Similar vs PLM", fontsize=14)
ax5.set_xlabel("Lifecycle Stages", fontsize=12)
ax5.set_ylabel("Rate of Sales (ROS)", fontsize=12)
ax5.set_ylim(0, max(ros_mean.max(), raw_ros_data.max()) + 0.5)
# ax5.grid(True, alpha=0.25)
ax5.legend(loc='upper right', fontsize=10)

# Show plot
st.pyplot(fig5)



