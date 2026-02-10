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