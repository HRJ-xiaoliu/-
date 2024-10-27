import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.font_manager as fm
import os

# Set Chinese font
# Here, "SimHei" (Black Font) is used as an example. Ensure this font is installed on your system.
# If using a different font, replace 'SimHei' with the corresponding font name.
plt.rcParams['font.family'] = 'SimHei'

# Prevent minus signs from appearing as squares
plt.rcParams['axes.unicode_minus'] = False

# Define activity data
data = {
    'Activity': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    'Description': [
        'Apply for Approval',
        'Construction/Implementation Plan',
        'Traffic Study Including Parking',
        'Service Availability Check',
        'Employee Report',
        'Committee Approval',
        'Construction/Implementation',
        'Occupancy'
    ],
    'Start Time': [0, 5, 5, 5, 20, 20, 30, 200],
    'Duration': [5, 15, 10, 5, 15, 10, 170, 35]
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate End Time (optional)
df['End Time'] = df['Start Time'] + df['Duration']

# Set colors (Critical Path activities in red, others in blue)
# Critical Path: A → B → F → G → H
critical_path = ['A', 'B', 'F', 'G', 'H']
colors = ['red' if activity in critical_path else 'blue' for activity in df['Activity']]

# Create Gantt Chart
fig, ax = plt.subplots(figsize=(12, 6))

# Plot each activity as a horizontal bar
for idx, row in df.iterrows():
    ax.barh(row['Activity'], row['Duration'], left=row['Start Time'], color=colors[idx], edgecolor='black')

# Add activity description labels
for idx, row in df.iterrows():
    ax.text(
        row['Start Time'] + row['Duration']/2,  # X position: midpoint of the bar
        row['Activity'],                       # Y position: activity name
        row['Description'],                    # Text to display
        va='center',                           # Vertical alignment: center
        ha='center',                           # Horizontal alignment: center
        color='black',                         # Set text color to black
        fontsize=9
    )

# Set Y-axis labels to activity names
ax.set_yticks(df['Activity'])
ax.set_yticklabels(df['Activity'])

# Add axis labels and title
ax.set_xlabel('Work Days', color='black')
ax.set_ylabel('Activity', color='black')
ax.set_title('Botanical Garden Playground Project Gantt Chart', color='black')

# Set X-axis and Y-axis tick label colors to black
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')

# Add grid
ax.grid(True, which='both', axis='x', linestyle='--', alpha=0.7)

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='red', edgecolor='black', label='Critical Path'),
    Patch(facecolor='blue', edgecolor='black', label='Non-Critical Path')
]
ax.legend(handles=legend_elements, loc='upper right')

# Adjust layout
plt.tight_layout()

# Display the chart
plt.show()

