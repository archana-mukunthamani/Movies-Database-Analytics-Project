# Final Dashboard


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.gridspec import GridSpec
from PIL import Image, ImageChops

# =========================
# DASHBOARD SETTINGS
# =========================

BG_COLOR = '#F2FAF7'
TITLE_COLOR = '#005F56'
TEXT_COLOR = '#1F2933'
BORDER_COLOR = '#009879'

chart_files = {
    "fig1": "Figure1_Top_Rated_Movies_By_Subscription_Status.png",
    "fig2": "Figure2_Most_Popular_Genres_By_Subscription_Status.png",
    "fig3": "Figure3_User_Distribution_by_Age_Group.png",
    "fig4": "Figure4_Distribution_of_Users_by_Subscription_Status.png",
    "fig5": "Figure5_User_Distribution_by_Country.png",
    "fig6": "Figure6_Device_Usage_Distribution_by_Subscription_Status.png"
}

# =========================
# HELPER FUNCTION
# =========================

def trim_image(path):
    img = Image.open(path).convert("RGB")
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()

    if bbox:
        img = img.crop(bbox)

    return img


def add_chart(ax, image_path):
    img = trim_image(image_path)
    ax.imshow(img)
    ax.axis("off")


# =========================
# CREATE DASHBOARD
# =========================

fig = plt.figure(figsize=(26, 18))
fig.patch.set_facecolor(BG_COLOR)

gs = GridSpec(
    3,
    3,
    width_ratios=[1.3,0.6,1.3],
    height_ratios=[1,1,1],
    hspace=0.02,
    wspace=0.02
)

# Top row
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 2])

# Middle row
ax3 = fig.add_subplot(gs[1, 0])
ax_text = fig.add_subplot(gs[1, 1])
ax4 = fig.add_subplot(gs[1, 2])

# Bottom row
ax5 = fig.add_subplot(gs[2, 0])
ax6 = fig.add_subplot(gs[2, 2])

# Add charts
add_chart(ax1, chart_files["fig1"])
add_chart(ax2, chart_files["fig2"])
add_chart(ax3, chart_files["fig3"])
add_chart(ax4, chart_files["fig4"])
add_chart(ax5, chart_files["fig5"])
add_chart(ax6, chart_files["fig6"])

# =========================
# INSIGHT PANEL
# =========================

ax_text.axis("off")

insights = (
    "KEY BUSINESS INSIGHTS\n\n"
    "Content Preferences\n"
    "• Drama and Comedy dominate total views.\n\n"
    "Subscriber Behaviour\n"
    "• Free and Subscriber users are nearly balanced.\n\n"
    "Audience Profile\n"
    "• Users aged 25–54 form the largest audience segment.\n\n"
    "Device Preferences\n"
    "• Mobile devices are the preferred viewing platform.\n\n"
    "Geographic Reach\n"
    "• User base is evenly distributed across countries."
)

ax_text.text(
    0.05,
    0.95,
    insights,
    fontsize=13,
    verticalalignment="top",
    color=TEXT_COLOR,
    linespacing=1.4,
    bbox=dict(
        facecolor="white",
        edgecolor=BORDER_COLOR,
        boxstyle="round,pad=0.8",
        linewidth=1.5
    )
)

# =========================
# MAIN TITLE
# =========================

fig.suptitle(
    "Movies Database – User Behaviour and Content Insights",
    fontsize=30,
    weight="bold",
    color=TITLE_COLOR,
    y=0.985
)

fig.text(
    0.5,
    0.01,
    'Source: Movies, Ratings and Users datasets | Python • SQL Server • Matplotlib',
    ha='center',
    fontsize=10,
    color='gray'
)
# =========================
# SAVE DASHBOARD
# =========================

plt.savefig(
    "Sprint2_Visualization_Dashboard_With_Insights.png",
    dpi=300,
    bbox_inches="tight",
    facecolor=BG_COLOR
)

plt.show()