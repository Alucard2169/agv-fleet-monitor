from ucimlrepo import fetch_ucirepo

dataset = fetch_ucirepo(id=601)  # AI4I 2020 Predictive Maintenance Dataset

X = dataset.data.features
y = dataset.data.targets

print("Features shape:", X.shape)
print("\nFeature columns:", list(X.columns))
print("\nTarget columns:", list(y.columns))
print("\nSample rows:\n", X.head())
print("\nFailure rate:", (y["Machine failure"].sum() / len(y)) * 100, "%")
print("\nFailure type breakdown:\n", y.drop(columns=["Machine failure"]).sum())
