import vectorbt as vbt
import yfinance as yf

# === 1. データ取得 (例: AAPL) ===
symbol = "AAPL"
data = yf.download(symbol, start="2020-01-01", end="2023-12-31")
print(data.head())

# vectorbtはCloseを使うので抽出
close = data["Close"]

# === 2. 戦略例: SMAクロス ===
fast_list = [10, 20]
slow_list = [50, 100]

# 移動平均
fast_ma = vbt.MA.run(close, window=fast_list)
slow_ma = vbt.MA.run(close, window=slow_list)

# シグナル生成
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# === 3. バックテスト実行 ===
pf = vbt.Portfolio.from_signals(
    close,
    entries,
    exits,
    fees=0.001,  # 手数料(0.1%)
    init_cash=100_000,  # 初期資金
)

# === 4. 結果出力 ===
print(pf.stats())  # 概要統計
print(pf.wrapper.columns)
pf.plot(column=(10, 50, "AAPL")).show()  # チャート表示
