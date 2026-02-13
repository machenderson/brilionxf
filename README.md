Analyzing **Fat-finger errors** (trade execution errors caused by human typing mistakes) is a fascinating niche in quantitative finance. These errors usually manifest as **extreme price spikes or drops** that revert almost instantly, creating a "needle" on the chart.

I’ve designed ​**"Brilionx FingerTrap"**​, a specialized tool that scans market data for these anomalies using a percentage-based threshold and volume analysis.

---

## 🛠️ Tool Name: Brilionx FingerTrap (v0.1)

This tool identifies potential fat-finger incidents by detecting price deviations that significantly exceed typical market volatility within a narrow timeframe.

### 1. Code File: `finger_trap.py`

Python

```
import numpy as np
import pandas as pd

class FingerTrap:
    """
    BrilionX Financial Tools: FingerTrap
    Anomaly detection for potential Fat-Finger execution errors.
    """
    def __init__(self, data):
        """
        :param data: Pandas DataFrame with ['Open', 'High', 'Low', 'Close', 'Volume']
        """
        self.data = data

    def detect_anomalies(self, threshold_sigma=5, volume_factor=3):
        """
        Detects anomalies based on price deviation and volume spikes.
        :param threshold_sigma: How many std deviations away from the mean return.
        :param volume_factor: Multiplier for average volume to confirm activity.
        """
        df = self.data.copy()
        
        # 1. Calculate Intraday Returns (High-Low Spread)
        df['shadow_percent'] = (df['High'] - df['Low']) / df['Low']
        
        # 2. Statistical Thresholding
        mean_shadow = df['shadow_percent'].mean()
        std_shadow = df['shadow_percent'].std()
        limit = mean_shadow + (threshold_sigma * std_shadow)
        
        # 3. Volume Confirmation (Errors often have unusual volume)
        avg_volume = df['Volume'].rolling(window=20).mean()
        
        # 4. Identification Logic
        anomalies = df[
            (df['shadow_percent'] > limit) & 
            (df['Volume'] > avg_volume * volume_factor)
        ]
        
        return anomalies

# --- BrilionX Demo Usage ---
if __name__ == "__main__":
    # Generating dummy market data with one "Fat-Finger" spike
    data_size = 100
    np.random.seed(7)
    
    dates = pd.date_range(start="2024-01-01", periods=data_size, freq='5min')
    prices = np.random.normal(150, 0.5, data_size)
    volumes = np.random.normal(1000, 100, data_size)
    
    df = pd.DataFrame({'Open': prices, 'High': prices+0.1, 'Low': prices-0.1, 'Close': prices, 'Volume': volumes}, index=dates)
    
    # Inject a Fat-Finger Error (Huge spike in price and volume at index 50)
    df.iloc[50, 1] = 185.0  # High price jumps significantly
    df.iloc[50, 4] = 8000.0 # Volume spikes
    
    ft = FingerTrap(df)
    results = ft.detect_anomalies()
    
    print(f"--- BrilionX FingerTrap Detection Report ---")
    if not results.empty:
        print(f"ALERT: Potential Fat-Finger detected at:")
        print(results[['High', 'Low', 'Volume', 'shadow_percent']])
    else:
        print("No significant anomalies detected.")
```

---

### 2. How it works (The Logic)

A Fat-Finger error is usually characterized by:

1. **Extreme Outlier:** The price reaches a level that is statistically impossible under normal "Random Walk" conditions.
2. **Mean Reversion:** The price returns to the "pre-error" level almost immediately (often within seconds or minutes).
3. **Volume Anomaly:** Because a large erroneous order was cleared, the volume at that specific tick is usually a massive multiple of the moving average.

---

### 3. Open Source Documentation (`README.md`)

> **Project:** Brilionx FingerTrap
> 
> **Author:** **BrilionX**
> 
> **Description:** A Python-based scanner to identify execution errors in high-frequency or historical OHLCV data.
> 
> **Core Detection Formula:**
> 
> We flag a data point as an anomaly if:
> 
> $$
> Spread_t > \mu_{spread} + (n \cdot \sigma_{spread})
> $$

AND

$$
Volume_t > k \cdot \text{SMA}(Volume)_{20}
$$

**Disclaimer:** This tool is for educational and research purposes. It helps identify "Bad Data" or "Execution Errors" that should be excluded from backtesting to avoid skewed results.

---

This tool is particularly useful for ​**cleaning your backtesting data**​, as Fat-Finger spikes can give you a false sense of "profit opportunities" that don't actually exist in a liquid market.

---
[Brilionx analyzer](https://https://github.com/machenderson/brilionxa)：This is a simple but powerful script that can evaluate asset performance based on historical return data.

[Brilionx FingerTrap](https://https://github.com/machenderson/brilionxf)：This tool identifies potential fat-finger incidents by detecting price deviations that significantly exceed typical market volatility within a narrow timeframe.

[Brilionx DataFetcher](https://https://github.com/machenderson/brilionxd)：The tool now includes a robust exporting feature to save your findings as persistent files.

[Brilionx CryptoPulse-Sentinel](https://https://github.com/machenderson/brilionxc)：This tool is divided into four distinct modules: ​Data Ingestion​, ​Quantitative Analysis​, ​Real-time Detection​, and ​Audit Export​.

---

### BrilionX, MEV, and Mindedge Venture: A Triumvirate of Stock Market Success Stories
