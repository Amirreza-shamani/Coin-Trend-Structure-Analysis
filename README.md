# Bitcoin Trend Structure Analysis

A Python-based data analysis project for studying Bitcoin price action through local peaks, valleys, and significant trend reversals.

## Project Overview

This project analyzes historical Bitcoin price data and attempts to simplify price action into a sequence of significant swing points.

The analysis includes:

* Local peak and valley detection
* Significant trend reversal detection
* Swing structure visualization
* Global high and low analysis
* Price action visualization
* A custom trend-structure dashboard

## Data

* **Asset:** BTC-USD
* **Source:** Yahoo Finance
* **Data:** Historical daily closing prices

## Technologies

* Python
* NumPy
* Pandas
* Matplotlib
* yfinance

## Method

The project first identifies local peaks and valleys by comparing each price with its immediate neighbors.

A configurable threshold (`alpha`) is then used to determine whether a price movement is significant enough to confirm a trend reversal.

```python
alpha = 0.04
```

The resulting swing points are visualized as a simplified representation of Bitcoin's price structure.

## Visualization

The dashboard contains four analytical views:

1. Price Action + Detected Trend Structure
2. Simplified Swing Path
3. Global Extremes
4. Local Peaks & Valleys
