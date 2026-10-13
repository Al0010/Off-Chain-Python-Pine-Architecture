import pandas as pd
import numpy as np

# 1. CSV loading 
filename = './data/OANDA_XAUUSD, 15.csv'
df = pd.read_csv(filename)
df.columns = [c.strip().lower() for c in df.columns] # Normalization 

# 2. TA metrics 
window_rolling_sma = 20 # Period SMA 
df['sma'] = df['close'].rolling(window=window_rolling_sma).mean() #SMA 

window_rolling_atr = 14 # Period ATR

# True Range + ATR
df['tr'] = np.maximum(
    df['high'] - df['low'],
    np.maximum(
        abs(df['high'] - df['close'].shift(1)),
        abs(df['low'] - df['close'].shift(1))
    )
)
df['atr'] = df['tr'].rolling(window=window_rolling_atr).mean()

df = df.dropna().reset_index(drop=True)

# 3. Backtesting 
def run_backtest(data, atr_mult, tp_pct):
    cash = 10000.0
    position = 0.0
    entry_price = 0.0
    trailing_stop = 0.0
    tp_price = 0.0
    
    for i in range(1, len(data)):
        row = data.iloc[i]
        prev = data.iloc[i-1]
        
        if position > 0:
            potential_ts = row['close'] - (row['atr'] * atr_mult)
            if potential_ts > trailing_stop:
                trailing_stop = potential_ts
                
            if row['low'] <= trailing_stop:
                cash = position * trailing_stop
                position = 0.0
            elif row['high'] >= tp_price:
                cash = position * tp_price
                position = 0.0
                
        if position == 0.0 and prev['close'] <= prev['sma'] and row['close'] > row['sma']:
            entry_price = row['close']
            position = cash / entry_price
            trailing_stop = entry_price - (row['atr'] * atr_mult)
            tp_price = entry_price * (1.0 + tp_pct / 100.0)
            
    final_val = position * data.iloc[-1]['close'] if position > 0 else cash
    return ((final_val - 10000.0) / 10000.0) * 100

# 4. Grid search params 
atr_grid = [0.5, 1, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
tp_grid = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

best_return = -999999
best_atr = 2.0
best_tp = 5.0

for am in atr_grid:
    for tp in tp_grid:
        ret = run_backtest(df, am, tp)
        if ret > best_return:
            best_return = ret
            best_atr = am
            best_tp = tp

# 5. Payload generation 
payload_string = f"{best_atr},{best_tp},{window_rolling_sma},{window_rolling_atr}"

print("==========================================")
print(f"Best ATR Multiplier : {best_atr}")
print(f"Best Take Profit %  : {best_tp}%")
print(f"Estimate Return     : {best_return:.2f}%")
print("==========================================")
print("\n--- COPY PAYLOAD AND PASTE ON TRADINGVIEW ---")
print(payload_string)
print("------------------------------------------------")