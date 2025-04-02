import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("all_over_stats.csv")

# Correlation matrix for key variables
correlation_matrix = df[["wicket_taken", "bowler_economy", "desirable_run_rate", "batter_strike_rate"]].corr()

# Heatmap of correlations
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Between Wickets and Other Factors")
plt.show()

# Box plot: Wickets vs Bowler Economy
plt.figure(figsize=(8, 5))
sns.boxplot(x="wicket_taken", y="bowler_economy", data=df)
plt.title("Bowler Economy vs Wickets Taken")
plt.xlabel("Wicket Taken (0 = No, 1 = Yes)")
plt.ylabel("Bowler Economy")
plt.show()

# Box plot: Wickets vs Desirable Run Rate
plt.figure(figsize=(8, 5))
sns.boxplot(x="wicket_taken", y="desirable_run_rate", data=df)
plt.title("Desirable Run Rate vs Wickets Taken")
plt.xlabel("Wicket Taken (0 = No, 1 = Yes)")
plt.ylabel("Desirable Run Rate")
plt.show()

# Box plot: Wickets vs Batter Strike Rate
plt.figure(figsize=(8, 5))
sns.boxplot(x="wicket_taken", y="batter_strike_rate", data=df)
plt.title("Batter Strike Rate vs Wickets Taken")
plt.xlabel("Wicket Taken (0 = No, 1 = Yes)")
plt.ylabel("Batter Strike Rate")
plt.show()

# Display correlation matrix
print("\nCorrelation Matrix:")
print(correlation_matrix)
