# Figure 2: Most Popular Genres

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
WITH GenreViews AS (
    SELECT
        u.SubscriptionStatus,
        TRIM(value) AS Genre,
        SUM(m.Total_Views) AS Total_Views
    FROM Users u
    JOIN Ratings r
        ON u.UserID = r.UserID
    JOIN Movies m
        ON r.MovieID = m.MovieID
    CROSS APPLY STRING_SPLIT(m.Genres, '|')
    GROUP BY
        u.SubscriptionStatus,
        TRIM(value)
),
TopGenres AS (
    SELECT TOP 10
        Genre,
        SUM(Total_Views) AS Overall_Total_Views
    FROM GenreViews
    GROUP BY Genre
    ORDER BY Overall_Total_Views DESC
)
SELECT
    gv.Genre,
    gv.SubscriptionStatus,
    gv.Total_Views
FROM GenreViews gv
JOIN TopGenres tg
    ON gv.Genre = tg.Genre
ORDER BY
    tg.Overall_Total_Views DESC,
    gv.SubscriptionStatus;
"""

df_genres = pd.read_sql(query, conn)
print(df_genres)

# Convert to pivot format
pivot_genres = df_genres.pivot(
    index='Genre',
    columns='SubscriptionStatus',
    values='Total_Views'
).fillna(0)

# Sort by total views across both Free and Subscriber
pivot_genres['Overall_Total_Views'] = pivot_genres.sum(axis=1)
pivot_genres = pivot_genres.sort_values(
    by='Overall_Total_Views',
    ascending=False
)

# Keep only top 10
pivot_genres = pivot_genres.head(10)

fig, ax = plt.subplots(figsize=FIG_SIZE)

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
                                  
y = np.arange(len(pivot_genres))
bar_height = 0.35

FREE_COLOR = '#009879'
SUBSCRIBER_COLOR = '#F4A261'

ax.barh(
    y - bar_height/2,
    pivot_genres.get('Free', 0),
    height=bar_height,
    label='Free',
    color=FREE_COLOR
)

ax.barh(
    y + bar_height/2,
    pivot_genres.get('Subscriber', 0),
    height=bar_height,
    label='Subscriber',
    color=SUBSCRIBER_COLOR
)

# Value labels
if 'Free' in pivot_genres.columns:
    for i, value in enumerate(pivot_genres['Free']):
        ax.text(
            value + 500000,
            y[i] - bar_height/2,
            f'{value/1_000_000:.1f}M',
            va='center',
            fontsize=9,
            color=TEXT_COLOR
        )

if 'Subscriber' in pivot_genres.columns:
    for i, value in enumerate(pivot_genres['Subscriber']):
        ax.text(
            value + 500000,
            y[i] + bar_height/2,
            f'{value/1_000_000:.1f}M',
            va='center',
            fontsize=9,
            color=TEXT_COLOR
        )

ax.set_yticks(y)
ax.set_yticklabels(pivot_genres.index)

ax.set_xlabel('Total Views (in Millions)', fontsize=LABEL_SIZE, color=TEXT_COLOR)
ax.set_title(
    'Most Popular Genres by Total Views and Subscription Status',
    fontsize=TITLE_SIZE,
    color=TITLE_COLOR,
    weight='bold'
)

plt.figtext(
    0.5,
    0.875,
    'Free vs Subscriber genre popularity comparison',
    ha='center',
    fontsize=9,
    color='#6B7280',
    style='italic'
)

ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x/1_000_000:.0f}M'))

ax.grid(axis='x', linestyle='--', alpha=0.4, color=GRID_COLOR)
ax.tick_params(axis='both', labelsize=TICK_SIZE, colors=TEXT_COLOR)

ax.legend(
    facecolor='white',
    edgecolor='lightgray',
    frameon=True
)

ax.invert_yaxis()

plt.figtext(
    0.5,
    0.02,
    'Note: Movies with multiple genres contribute views to each associated genre.',
    ha='center',
    fontsize=9,
    style='italic',
    color=TITLE_COLOR
)

plt.tight_layout(rect=[0, 0.03, 0.9, 0.95])
plt.savefig('Figure2_Most_Popular_Genres_By_Subscription_Status.png', dpi=300, bbox_inches='tight')
plt.show()
