#Figure 1. Top 10 Highest Rated Movies

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
WITH TopMovies AS (
    SELECT TOP 10
        m.MovieID,
        m.Title,
        ROUND(AVG(r.Rating), 2) AS Overall_Average_Rating,
        COUNT(r.RatingID) AS Total_Ratings
    FROM Ratings r
    JOIN Movies m
        ON r.MovieID = m.MovieID
    GROUP BY m.MovieID, m.Title
    HAVING COUNT(r.RatingID) >= 5
    ORDER BY Overall_Average_Rating DESC
)
SELECT
    tm.Title,
    tm.Overall_Average_Rating,
    u.SubscriptionStatus,
    ROUND(AVG(r.Rating), 2) AS Average_Rating,
    COUNT(r.RatingID) AS Number_of_Ratings
FROM TopMovies tm
JOIN Ratings r
    ON tm.MovieID = r.MovieID
JOIN Users u
    ON r.UserID = u.UserID
GROUP BY
    tm.Title,
    tm.Overall_Average_Rating,
    u.SubscriptionStatus
ORDER BY
    tm.Overall_Average_Rating DESC,
    u.SubscriptionStatus;
"""

df_movies = pd.read_sql(query, conn)

print(df_movies)

# Convert to pivot format
pivot_df = df_movies.pivot(
    index='Title',
    columns='SubscriptionStatus',
    values='Average_Rating'
).fillna(0)

movie_order = (
    df_movies[['Title', 'Overall_Average_Rating']]
    .drop_duplicates()
    .sort_values(
        by='Overall_Average_Rating',
        ascending=False
    )
)

pivot_df = pivot_df.reindex(movie_order['Title'])

fig, ax = plt.subplots(figsize=(12, 8))

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

y = np.arange(len(pivot_df))
bar_height = 0.30

ax.barh(y - bar_height/2, pivot_df.get('Free', 0), height=bar_height, label='Free', color=FREE_COLOR)
ax.barh(y + bar_height/2, pivot_df.get('Subscriber', 0), height=bar_height, label='Subscriber', color=SUBSCRIBER_COLOR)

if 'Free' in pivot_df.columns:
    for i, value in enumerate(pivot_df['Free']):
        ax.text(value + 0.03, y[i] - bar_height/2, f'{value:.2f}', va='center', fontsize=9, color=TEXT_COLOR)

if 'Subscriber' in pivot_df.columns:
    for i, value in enumerate(pivot_df['Subscriber']):
        ax.text(value + 0.03, y[i] + bar_height/2, f'{value:.2f}', va='center', fontsize=9, color=TEXT_COLOR)

ax.set_yticks(y)
ax.set_yticklabels(pivot_df.index)


ax.set_title(
    'Top Rated Movies by Subscription Status',
    fontsize=TITLE_SIZE,
    color=TITLE_COLOR,
    weight='bold'
)
plt.figtext(
    0.5,
    0.875,
    'Free vs Subscriber ratings comparison',
    ha='center',
    fontsize=9,
    style='italic',
    color='#6B7280'
)
ax.set_xlabel('Average Rating', fontsize=LABEL_SIZE, color=TEXT_COLOR)
ax.set_xlim(0, 5.5)
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
    'Note: Movies with fewer than 5 ratings were excluded to ensure meaningful comparisons.',
    ha='center',
    fontsize=9,
    style='italic',
    color=TITLE_COLOR
)
plt.tight_layout(rect=[0,0.03,0.9,0.95])
plt.savefig('Figure1_Top_Rated_Movies_By_Subscription_Status.png', dpi=300, bbox_inches='tight')
plt.show()