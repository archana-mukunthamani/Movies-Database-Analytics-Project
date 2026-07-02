# Figure 3: User Distribution by Age Group and Subscription Status using two pie charts side by side.

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
    CASE
        WHEN Age < 18 THEN 'Under 18'
        WHEN Age BETWEEN 18 AND 24 THEN '18-24'
        WHEN Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55+'
    END AS Age_Group,
    COUNT(UserID) AS User_Count
FROM Users
GROUP BY
    SubscriptionStatus,
    CASE
        WHEN Age < 18 THEN 'Under 18'
        WHEN Age BETWEEN 18 AND 24 THEN '18-24'
        WHEN Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55+'
    END
ORDER BY
    SubscriptionStatus,
    Age_Group;
"""

df_age = pd.read_sql(query, conn)

free_df = df_age[df_age['SubscriptionStatus'] == 'Free']
subscriber_df = df_age[df_age['SubscriptionStatus'] == 'Subscriber']

AGE_COLORS = [
    '#009879',  # Teal
    '#4DB6AC',
    '#80CBC4',
    '#AED581',
    '#FFD54F',
    '#F4A261'
]

fig, axes = plt.subplots(1, 2, figsize=(14, 7))

fig.patch.set_facecolor(BG_COLOR)

# Free users
axes[0].pie(
    free_df['User_Count'],
    labels=free_df['Age_Group'],
    autopct='%1.1f%%',
    colors=AGE_COLORS,
    startangle=90,
    wedgeprops=dict(width=0.4, edgecolor='white')
)

axes[0].set_title(
    'Free Users',
    fontsize=14,
    color=TITLE_COLOR,
    weight='bold'
)
# Add total users in center
axes[0].text(
    0, 0,
    f"{free_df['User_Count'].sum():,}\nUsers",
    ha='center',
    va='center',
    fontsize=12,
    weight='bold',
    color=TITLE_COLOR
)
# Subscriber users
axes[1].pie(
    subscriber_df['User_Count'],
    labels=subscriber_df['Age_Group'],
    autopct='%1.1f%%',
    colors=AGE_COLORS,
    startangle=90,
    wedgeprops=dict(width=0.4, edgecolor='white')
)

axes[1].set_title(
    'Subscriber Users',
    fontsize=14,
    color=TITLE_COLOR,
    weight='bold'
)

# Add total users in center
axes[1].text(
    0, 0,
    f"{subscriber_df['User_Count'].sum():,}\nUsers",
    ha='center',
    va='center',
    fontsize=12,
    weight='bold',
    color=TITLE_COLOR
)

# Main title
fig.suptitle(
    'User Distribution by Age Group and Subscription Status',
    fontsize=18,
    color=TITLE_COLOR,
    weight='bold'
)

# Subtitle
plt.figtext(
    0.5,
    0.875,
    'Comparison of age distribution between Free and Subscriber users',
    ha='center',
    fontsize=9,
    color='#6B7280',
    style='italic'
)

# Bottom note
plt.figtext(
    0.5,
    0.02,
    'Note: Percentages represent the proportion of users within each subscription category.',
    ha='center',
    fontsize=9,
    style='italic',
    color=TITLE_COLOR
)

plt.tight_layout(rect=[0, 0.05, 1, 0.92])

plt.savefig(
    'Figure3_User_Distribution_by_Age_Group.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()