import numpy as np
import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt

#region Configuration

ticker = "SOL-USD"

start_date = "2020-12-29"
end_date = "2026-09-29"

alpha = 0.04

#endregion

#region Read Data

df = yf.download(
    ticker,
    start=start_date,
    end=end_date,
    multi_level_index=False
)

close = df["Close"]
x = np.arange(len(close))

#endregion

# region Create Figure

plt.style.use("dark_background")

fig = plt.figure(figsize=(15, 9), facecolor="#0b0f14")

gs = fig.add_gridspec(
    3, 2,
    height_ratios=[2.2, 1.25, 1.25],
    hspace=0.32,
    wspace=0.18
)

ax0 = fig.add_subplot(gs[0, :])
ax1 = fig.add_subplot(gs[1, :])
ax2 = fig.add_subplot(gs[2, 0])
ax3 = fig.add_subplot(gs[2, 1])

# Dashboard title
fig.suptitle(
    f"{ticker} • TREND STRUCTURE ANALYSIS",
    fontsize=20,
    fontweight="bold",
    x=0.05,
    y=0.97,
    ha="left"
)

# Panel styling
axes = [ax0, ax1, ax2, ax3]

for ax in axes:
    ax.set_facecolor("#11161d")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.grid(
        True,
        alpha=0.12,
        linestyle="--",
        linewidth=0.7
    )

    ax.tick_params(
        colors="#aeb7c2",
        labelsize=9
    )

    for spine in ax.spines.values():
        spine.set_alpha(0.25)

# endregion

# region ax0 ax1 Trend Line

# region search for peak and valley

swing_x = []
swing_y = []
swing_type = []

for i in range(1, len(close) - 1):
    if close.iloc[i - 1] < close.iloc[i] > close.iloc[i + 1]:
        swing_type.append("peak")
    elif close.iloc[i - 1] > close.iloc[i] < close.iloc[i + 1]:
        swing_type.append("valley")
    else:
        continue

    swing_x.append(i)
    swing_y.append(close.iloc[i])

# endregion

x_trend = [x.min()]
y_trend = [close.iloc[0]]

reference = close.iloc[0]

temp = None

# region expected type

peak_score = 0
valley_score = 0
last_data_peak = close.iloc[0]
last_data_valley = close.iloc[0]

for i in range(min(10, len(swing_type))):
    if swing_type[i] == "peak":

        if swing_y[i] > last_data_peak:
            peak_score += 1
            last_data_peak = swing_y[i]
        else:
            valley_score += 1


    else:
        if swing_y[i] < last_data_valley:
            valley_score += 1
            last_data_valley = swing_y[i]
        else:
            peak_score += 1

text = ("peak" if peak_score >= valley_score else "valley")
print(text)
expected_type = text

# endregion

# region fig text

fig.text(0.72, 0.955, f"ASSET  →  {ticker}", fontsize=11, fontweight="bold", ha="center")

fig.text(0.72, 0.925,
         f"DATA POINTS  →  {len(close):,}    |    PERIOD  →  {pd.Timestamp(close.index[0]).date()} → {pd.Timestamp(close.index[-1]).date()}",
         fontsize=9, alpha=0.7, ha="center")

# endregion

# region x/Y Trend

for day, price, t in zip(swing_x, swing_y, swing_type):
    if expected_type == "peak" and t == "peak":
        if price > reference:
            reference = price
            temp = day
        elif price < reference * (1 - alpha):
            expected_type = "valley"
            y_trend.append(reference)
            x_trend.append(temp)
    elif expected_type == "valley" and t == "valley":
        if price < reference:
            reference = price
            temp = day
        elif price > reference * (1 + alpha):
            expected_type = "peak"
            y_trend.append(reference)
            x_trend.append(temp)

x_trend.append(x.max())
y_trend.append(close.iloc[-1])

# endregion

# region ax0
ax0.set_title("PRICE ACTION + DETECTED TREND STRUCTURE", loc="left", fontsize=11, fontweight="bold", pad=12)

ax0.plot(x, close, linewidth=2, alpha=1, color="w")

ax0.plot(x_trend, y_trend, linewidth=1, marker="o", markersize=3, color="#e8a619")

ax0.set_ylabel(f"{ticker} Price", alpha=0.7)

ax0.text(
    0.99, 0.92,
    f"{len(x_trend) - 2} swings detected",
    transform=ax0.transAxes,
    ha="right",
    fontsize=9,
    alpha=0.6
)

# endregion

# region ax1

ax1.set_title("SIMPLIFIED SWING PATH", loc="left", fontsize=11, fontweight="bold", pad=10)

ax1.plot(x_trend, y_trend, linewidth=2.5, color="#e8a619")

ax1.set_ylabel("Price", alpha=0.7)

# endregion


# endregion

# region ax2 start -> min/max -> max/min -> end

start_point = (x.min(), close.iloc[0])  # (x1,y1)
highest_point = (close.argmax(), close.max())
lowest_point = (close.argmin(), close.min())
end_point = (x.max(), close.iloc[-1])  # (x2,y2)

if highest_point[0] > lowest_point[0]:
    highest_point, lowest_point = lowest_point, highest_point

ax2.set_title("GLOBAL EXTREMES", loc="left", fontsize=11, fontweight="bold", pad=10)

ax2.plot(x, close, linewidth=1, alpha=0.45)

ax2.plot(
    [start_point[0], highest_point[0], lowest_point[0], end_point[0]],
    [start_point[1], highest_point[1], lowest_point[1], end_point[1]],
    marker="o",
    linestyle="-",
    linewidth=2
)

ax2.set_ylabel("Price", alpha=0.7)

# endregion

# region ax3 All Peaks & Valleys

ax3.set_title(
    "LOCAL PEAKS & VALLEYS",
    loc="left",
    fontsize=11,
    fontweight="bold",
    pad=10
)

ax3.plot(
    x,
    close,
    linewidth=1,
    alpha=0.5
)

ax3.scatter(
    swing_x,
    swing_y,
    s=18,
    alpha=0.8
)

ax3.set_ylabel("Price", alpha=0.7)
# endregion

plt.savefig(
    "../images/sol_trend_dashboard.png",
    dpi=200,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)

plt.show()
