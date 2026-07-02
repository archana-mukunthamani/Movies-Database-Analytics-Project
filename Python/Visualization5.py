# Figure 5. User Distribution by Country and Subscription Status

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
    Country,
    SubscriptionStatus,
    COUNT(UserID) AS User_Count
FROM Users
GROUP BY
    Country,
    SubscriptionStatus
ORDER BY
    Country,
    SubscriptionStatus;
"""

df_country = pd.read_sql(query, conn)
print(df_country)

# Convert to pivot format

pivot_country = df_country.pivot(
    index='Country',
    columns='SubscriptionStatus',
    values='User_Count'
).fillna(0)

# Sort countries by total users
pivot_country['Total_Users'] = pivot_country.sum(axis=1)
pivot_country = pivot_country.sort_values(
    by='Total_Users',
    ascending=False
)

# Remove helper column
pivot_country = pivot_country.drop(columns=['Total_Users'])

# Create the chart

fig, ax = plt.subplots(figsize=(12,7))

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

y = np.arange(len(pivot_country))
bar_height = 0.35

ax.barh(
    y - bar_height/2,
    pivot_country.get('Free', 0),
    height=bar_height,
    label='Free',
    color=FREE_COLOR
)

ax.barh(
    y + bar_height/2,
    pivot_country.get('Subscriber', 0),
    height=bar_height,
    label='Subscriber',
    color=SUBSCRIBER_COLOR
)

# Value labels
if 'Free' in pivot_country.columns:
    for i, value in enumerate(pivot_country['Free']):
        ax.text(
            value + 5,
            y[i]-bar_height/2,
            str(int(value)),
            va='center',
            fontsize=9,
            color=TEXT_COLOR
        )

if 'Subscriber' in pivot_country.columns:
    for i, value in enumerate(pivot_country['Subscriber']):
        ax.text(
            value + 5,
            y[i]+bar_height/2,
            str(int(value)),
            va='center',
            fontsize=9,
            color=TEXT_COLOR
        )

ax.set_yticks(y)
ax.set_yticklabels(pivot_country.index)

ax.set_xlabel(
    'Number of Users',
    fontsize=LABEL_SIZE,
    color=TEXT_COLOR
)

ax.set_title(
    'User Distribution by Country and Subscription Status',
    fontsize=TITLE_SIZE,
    color=TITLE_COLOR,
    weight='bold'
)

plt.figtext(
    0.5,
    0.875,
    'Comparison of Free and Subscriber users across countries',
    ha='center',
    fontsize=9,
    color='#6B7280',
    style='italic'
)

ax.grid(axis='x', linestyle='--', alpha=0.4, color=GRID_COLOR)

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

ax.invert_yaxis()

plt.figtext(
    0.5,
    0.02,
    'Note: User counts represent the number of registered users in each country.',
    ha='center',
    fontsize=9,
    style='italic',
    color=TITLE_COLOR
)

plt.tight_layout(rect=[0,0.04,0.9,0.95])

plt.savefig(
    'Figure5_User_Distribution_by_Country.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()