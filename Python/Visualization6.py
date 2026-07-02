# Figure 6: Device Usage Distribution among users by Subscription Status

import pandas as pd
import pyodbc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# =========================
# THEME SETTINGS
# =========================
THEME_COLOR = '#009879'
BG_COLOR = '#F2FAF7'
GRID_COLOR = '#BFD8D3'
TITLE_COLOR = '#005F56'
TEXT_COLOR = '#1F2933'
FREE_COLOR = '#009879'      # Teal Green
SUBSCRIBER_COLOR = '#F4A261'   # Soft Orange

FIG_SIZE = (12, 7)
TITLE_SIZE = 18
LABEL_SIZE = 11
TICK_SIZE = 10

conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=.;'
    r'DATABASE=Movies_db;'
    r'Trusted_Connection=yes;'
)

query = """
SELECT
    Device,
    SubscriptionStatus,
    COUNT(UserID) AS User_Count
FROM Users
GROUP BY
    Device,
    SubscriptionStatus
ORDER BY
    Device,
    SubscriptionStatus;
"""
# lOAD dATA
df_device = pd.read_sql(query, conn)

print(df_device)

# Convert to pivot format
pivot_device = df_device.pivot(
    index='Device',
    columns='SubscriptionStatus',
    values='User_Count'
).fillna(0)

# Sort devices by total users
pivot_device['Total_Users'] = pivot_device.sum(axis=1)

pivot_device = pivot_device.sort_values(
    by='Total_Users',
    ascending=False
)

pivot_device = pivot_device.drop(columns=['Total_Users'])

# Create Grouped Vertical Bar Chart

fig, ax = plt.subplots(figsize=(10,7))

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

# Remove top and right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Optional: make remaining borders subtle
ax.spines['left'].set_color('#6B7280')
ax.spines['bottom'].set_color('#6B7280')
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_linewidth(0.8)

x = np.arange(len(pivot_device))
bar_width = 0.25

bars1 = ax.bar(
    x - bar_width/2,
    pivot_device.get('Free',0),
    width=bar_width,
    color=FREE_COLOR,
    label='Free'
)

bars2 = ax.bar(
    x + bar_width/2,
    pivot_device.get('Subscriber',0),
    width=bar_width,
    color=SUBSCRIBER_COLOR,
    label='Subscriber'
)

# Add values on bars
for bar in bars1:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        height + 5,
        f'{int(height)}',
        ha='center',
        fontsize=9,
        color=TEXT_COLOR
    )

for bar in bars2:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        height + 5,
        f'{int(height)}',
        ha='center',
        fontsize=9,
        color=TEXT_COLOR
    )

ax.set_xticks(x)
ax.set_xticklabels(pivot_device.index)

ax.set_ylabel(
    'Number of Users',
    fontsize=LABEL_SIZE,
    color=TEXT_COLOR
)

ax.set_title(
    'Device Usage Distribution by Subscription Status',
    fontsize=TITLE_SIZE,
    color=TITLE_COLOR,
    weight='bold'
)

plt.figtext(
    0.5,
    0.865,
    'Comparison of device preferences between Free and Subscriber users',
    ha='center',
    fontsize=9,
    color='#6B7280',
    style='italic'
)

ax.grid(axis='y',
        linestyle='--',
        alpha=0.4,
        color=GRID_COLOR)

ax.tick_params(
    axis='both',
    labelsize=TICK_SIZE,
    colors=TEXT_COLOR
)

ax.legend(
    facecolor='white',
    edgecolor='lightgray',
    frameon=True
)

plt.figtext(
    0.5,
    0.02,
    'Note: User counts represent the number of users using each device type.',
    ha='center',
    fontsize=9,
    style='italic',
    color=TITLE_COLOR
)

plt.tight_layout(rect=[0,0.04,1,0.95])

plt.savefig(
    'Figure6_Device_Usage_Distribution_by_Subscription_Status.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()