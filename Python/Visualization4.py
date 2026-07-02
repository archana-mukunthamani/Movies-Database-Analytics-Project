# Figure 4: Distribution of Users by Subscription Status

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
    SubscriptionStatus,
    COUNT(*) AS User_Count
FROM Users
GROUP BY SubscriptionStatus;
"""
df_subscription = pd.read_sql(query, conn)
conn.close()

print(df_subscription)

fig, ax = plt.subplots(figsize=(8,8))

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

colors = ['#009879', '#F4A261']

ax.pie(
    df_subscription['User_Count'],
    labels=df_subscription['SubscriptionStatus'],
    autopct='%1.1f%%',
    pctdistance=0.75,        # Position percentages inside the ring
    startangle=90,
    colors=colors,
    wedgeprops=dict(width=0.4, edgecolor='white'),
    textprops={
        'fontsize': 12,
        'color': 'black',
        'weight': 'bold'
    }
)

# Center text
ax.text(
    0,
    0,
    f"{df_subscription['User_Count'].sum():,}\nUsers",
    ha='center',
    va='center',
    fontsize=16,
    weight='bold',
    color=TITLE_COLOR
)

ax.set_title(
    'Distribution of Users by Subscription Status',
    fontsize=18,
    color=TITLE_COLOR,
    weight='bold'
)

plt.figtext(
    0.5,
    0.875,
    'Comparison of Free and Subscriber user segments',
    ha='center',
    fontsize=9,
    color='#6B7280',
    style='italic'
)

plt.figtext(
    0.5,
    0.02,
    'Note: Percentages represent the proportion of total users.',
    ha='center',
    fontsize=9,
    style='italic',
    color=TITLE_COLOR
)

plt.tight_layout(rect=[0,0.05,1,0.95])

plt.savefig(
    'Figure4_Distribution_of_Users_by_Subscription_Status.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()