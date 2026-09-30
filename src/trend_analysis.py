import numpy as np
import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt

#region Read Data

ticker = "BTC-USD"
df = yf.download(ticker, start="2020-12-29", end="2026-09-29", multi_level_index=False)

close = df["Close"]
X = np.arange(len(close))

#endregion

# region figure and gridspec

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

# region search for peak and vally

swing_X = []
swing_Y = []
swing_Type = []

for i in range(1, len(close) - 1):
    if close.iloc[i - 1] < close.iloc[i] > close.iloc[i + 1]:
        swing_Type.append("peak")
    elif close.iloc[i - 1] > close.iloc[i] < close.iloc[i + 1]:
        swing_Type.append("vally")
    else:
        continue

    swing_X.append(i)
    swing_Y.append(close.iloc[i])

# endregion

X_trend = [X.min()]
Y_trend = [close.iloc[0]]

reference = close.iloc[0]

alpha = 0.04
temp = None

# region expected type

peak_score = 0
vally_score = 0
last_data_peak = close.iloc[0]
last_data_vally = close.iloc[0]

for i in range(min(10, len(swing_Type))):
    if swing_Type[i] == "peak":

        if swing_Y[i] > last_data_peak:
            peak_score += 1
            last_data_peak = swing_Y[i]
        else:
            vally_score += 1


    else:
        if swing_Y[i] < last_data_vally:
            vally_score += 1
            last_data_vally = swing_Y[i]
        else:
            peak_score += 1

text = ("peak" if peak_score >= vally_score else "vally")
print(text)
expected_type = text

# endregion

# region fig text

fig.text(0.72, 0.955, f"ASSET  →  {ticker}", fontsize=11, fontweight="bold", ha="center")

fig.text(0.72, 0.925,
         f"DATA POINTS  →  {len(close):,}    |    PERIOD  →  {pd.Timestamp(close.index[0]).date()} → {pd.Timestamp(close.index[-1]).date()}",
         fontsize=9, alpha=0.7, ha="center")

# endregion

# region X/Y Trend

for day, price, t in zip(swing_X, swing_Y, swing_Type):
    if expected_type == "peak" and t == "peak":
        if price > reference:
            reference = price
            temp = day
        elif price < reference * (1 - alpha):
            expected_type = "vally"
            Y_trend.append(reference)
            X_trend.append(temp)
    elif expected_type == "vally" and t == "vally":
        if price < reference:
            reference = price
            temp = day
        elif price > reference * (1 + alpha):
            expected_type = "peak"
            Y_trend.append(reference)
            X_trend.append(temp)

X_trend.append(X.max())
Y_trend.append(close.iloc[-1])

# endregion

# region ax0
ax0.set_title("PRICE ACTION + DETECTED TREND STRUCTURE", loc="left", fontsize=11, fontweight="bold", pad=12)

ax0.plot(X, close, linewidth=2, alpha=1, color="w")

ax0.plot(X_trend, Y_trend, linewidth=1, marker="o", markersize=3, color="#e8a619")

ax0.set_ylabel(f"{ticker} Price", alpha=0.7)

ax0.text(
    0.99, 0.92,
    f"{len(X_trend) - 2} swings detected",
    transform=ax0.transAxes,
    ha="right",
    fontsize=9,
    alpha=0.6
)

# endregion

# region ax1

ax1.set_title("SIMPLIFIED SWING PATH", loc="left", fontsize=11, fontweight="bold", pad=10)

ax1.plot(X_trend, Y_trend, linewidth=2.5, color="#e8a619")

ax1.set_ylabel("Price", alpha=0.7)

# endregion


# endregion

# region ax2 start -> min/max -> max/min -> end

start_point = (X.min(), close.iloc[0])  # (x1,y1)
max_point = (close.argmax(), close.max())
min_point = (close.argmin(), close.min())
end_point = (X.max(), close.iloc[-1])  # (x2,y2)

if max_point[0] > min_point[0]:
    max_point, min_point = min_point, max_point

ax2.set_title("GLOBAL EXTREMES", loc="left", fontsize=11, fontweight="bold", pad=10)

ax2.plot(X, close, linewidth=1, alpha=0.45)

ax2.plot(
    [start_point[0], max_point[0], min_point[0], end_point[0]],
    [start_point[1], max_point[1], min_point[1], end_point[1]],
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
    X,
    close,
    linewidth=1,
    alpha=0.5
)

ax3.scatter(
    swing_X,
    swing_Y,
    s=18,
    alpha=0.8
)

ax3.set_ylabel("Price", alpha=0.7)
# endregion

plt.savefig(
    "../images/btc_trend_dashboard.png",
    dpi=200,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)

plt.show()
