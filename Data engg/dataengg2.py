import pandas as pd
import matplotlib.pyplot as plt
import itertools

# Load the dataset (assuming it's already loaded as df)
df = pd.read_csv('Data engg/over_features.csv')

# Choose a set of features to investigate.
# You can modify this list to include different combinations.
features = ['over', 'number_of_wickets_lost', 'required_desired_run_rate', 'dot_ball_pressure']

# Generate scatter plots for each pair of features.
for feat1, feat2 in itertools.combinations(features, 2):
    plt.figure(figsize=(8, 6))
    # Plot data points for each value of wicket_next_over (0 and 1)
    for wicket in [0, 1]:
        subset = df[df['wicket_next_over'] == wicket]
        plt.scatter(subset[feat1], subset[feat2], alpha=0.6, label=f'wicket_next_over = {wicket}')
    plt.xlabel(feat1)
    plt.ylabel(feat2)
    plt.title(f"Scatter plot: {feat1} vs {feat2}")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Check the class distribution of wicket_next_over
wicket_counts = df['wicket_next_over'].value_counts()
print("Distribution of wicket_next_over:")
print(wicket_counts)

# Plot the distribution using matplotlib
import matplotlib.pyplot as plt

plt.figure(figsize=(6,4))
plt.bar(wicket_counts.index.astype(str), wicket_counts.values, color='skyblue')
plt.xlabel("wicket_next_over")
plt.ylabel("Count")
plt.title("Distribution of wicket_next_over")
plt.show()

