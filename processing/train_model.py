import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv("data/merged_gold_data.csv")
df = df.dropna()
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

n_lags = 5

features = [col for col in df.columns if col.startswith("dxy_") or col.startswith("sp500_") or col.startswith("gold_")]
features = [f for f in features if f not in ["gold_last", "gold_change_percent"]]

for feat in features:
    for lag in range(1, n_lags + 1):
        df[f"{feat}_lag_{lag}"] = df[feat].shift(lag)


df["target"] = df["gold_last"].shift(-1)
df = df.dropna()

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df = df[(df[col] >= lower) & (df[col] <= upper)]

split_index = int(len(df) * 0.7)
train_df = df.iloc[:split_index]
test_df = df.iloc[split_index:]

X_train = train_df.drop(columns=["Date", "target", "gold_last", "gold_change_percent"])
y_train = train_df["target"]
X_test = test_df.drop(columns=["Date", "target", "gold_last", "gold_change_percent"])
y_test = test_df["target"]

print(f"Số đặc trưng đầu vào: {X_train.shape[1]}")
print(f"Số mẫu train: {len(X_train)}, test: {len(X_test)}")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42)
}

results = []

for name, model in models.items():
    X_train_input = X_train_scaled if name != "Decision Tree" else X_train
    X_test_input = X_test_scaled if name != "Decision Tree" else X_test

    model.fit(X_train_input, y_train)

    preds_train = model.predict(X_train_input)
    preds_test = model.predict(X_test_input)

    mae = mean_absolute_error(y_test, preds_test)
    mse = mean_squared_error(y_test, preds_test)
    rmse = np.sqrt(mse)
    r2_test = r2_score(y_test, preds_test)

    r2_train = r2_score(y_train, preds_train)

    accuracy = 1 - (mae / y_test.mean())

    print(f"\nMô hình: {name}")
    print(f"MAE  : {mae:.4f}")
    print(f"MSE  : {mse:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R2 Test : {r2_test:.4f}")
    print(f"R2 Train: {r2_train:.4f}")
    print(f"Accuracy: {accuracy:.4f}")

    overfit_status = "Tốt"
    if r2_train - r2_test > 0.1:
        overfit_status = "Overfit"
    elif r2_test - r2_train > 0.1:
        overfit_status = "Underfit"

    results.append({
        "Model": name,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2 Test": r2_test,
        "R2 Train": r2_train,
        "Accuracy": accuracy,
        "Fit Status": overfit_status
    })

# In bảng so sánh
df_result = pd.DataFrame(results).sort_values("R2 Test", ascending=False)
print("\n Bảng so sánh mô hình:")
print(df_result.to_string(index=False))
