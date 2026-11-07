import pandas as pd
from mlkit.config import DATA_RAW

# Load customer dataset
df = pd.read_csv(DATA_RAW / "customers.csv")

print("Dataset loaded successfully!")
print(df.head())
print(df.columns)

# Clean Plan names
df["Plan"] = df["Plan"].str.strip().str.title()

# Calculate churn rate and average monthly charges
result = df.groupby("Plan").agg(
    churn_rate=("Churn", "mean"),
    avg_charges=("Monthly Charges", "mean")
)

# Convert churn rate into percentage
result["churn_rate"] = result["churn_rate"] * 100

print("\nPlan-wise Analysis:")
print(result.round(2))

print("\nHighest Churn Rate Plan:")
print(result["churn_rate"].idxmax())

print("\nHighest Average Charges Plan:")
print(result["avg_charges"].idxmax())




# Q2: Compare Mean and Median Imputation

# Calculate mean and median
mean_value = df["Monthly Charges"].mean()
median_value = df["Monthly Charges"].median()

# Create two copies
df_mean = df.copy()
df_median = df.copy()

# Fill missing values
df_mean["Monthly Charges"] = df_mean["Monthly Charges"].fillna(mean_value)
df_median["Monthly Charges"] = df_median["Monthly Charges"].fillna(median_value)

# Display comparison
print("\nMean vs Median Imputation")
print("Mean value:", round(mean_value, 2))
print("Median value:", round(median_value, 2))

print("Mean imputation average:",
      round(df_mean["Monthly Charges"].mean(), 2))

print("Median imputation average:",
      round(df_median["Monthly Charges"].mean(), 2))

print("Missing values after mean imputation:",
      df_mean["Monthly Charges"].isna().sum())

print("Missing values after median imputation:",
      df_median["Monthly Charges"].isna().sum())



# Q3: Schema validation

from mlkit.validation import validate, ValidationError

# Define schema
SCHEMA = {
    "Logins Per Week": {
        "min": 0,
        "max": 50,
        "nullable": False
    }
}

# First, validate the original dataset
print("\nTesting original dataset:")
try:
    validate(df, SCHEMA)
    print("Validation passed!")
except ValidationError as e:
    print("Validation failed:", e)


# Break the rule intentionally
df_test = df.copy()
df_test.loc[0, "Logins Per Week"] = 60

print("\nTesting modified dataset:")
try:
    validate(df_test, SCHEMA)
    print("Validation passed!")
except ValidationError as e:
    print("Validation failed:", e)