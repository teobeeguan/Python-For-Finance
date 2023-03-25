import yfinance as yf
from sklearn.linear_model import LogisticRegression

df = yf.download("^GSPC", start="2012-01-01", end="2022-12-31")

df_filter = df["Adj Close"].pct_change() * 100
df_filter = df_filter.rename("Today")
df_filter = df_filter.reset_index()
 
df_filter["Volume"] = df["Volume"].shift(1).values / 1000_000_000

for i in range(1,6):
    df_filter["Lag " + str(i)] = df_filter["Today"].shift(i)

df_filter = df_filter.dropna()
    
df_filter["Direction"] = [1 if i > 0 else 0 for i in df_filter["Today"]]

X = df_filter[["Lag 1", "Lag 2", "Lag 3", "Lag 4", "Lag 5", "Volume"]]
y = df_filter[["Direction"]]

X_train = X[0:2000]
X_test = X[2000:]

y_train = y[0:2000]
y_test = y[2000:]

clf = LogisticRegression().fit(X_train, y_train)

clf.score(X_test, y_test)
