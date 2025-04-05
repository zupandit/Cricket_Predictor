import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
df = pd.read_csv('/Users/familyaccount/Documents/544 Project/Cricket_Predictor/Data engg/over_features.csv')

# Compute correlation matrix
# We select only the numeric columns to compute correlations.
numeric_df = df.select_dtypes(include=[np.number])
correlation_matrix = numeric_df.corr()

# Visualize the correlation matrix
plt.figure(figsize=(12, 10))
# Use imshow for the heatmap
plt.imshow(correlation_matrix, cmap='viridis', interpolation='none')
plt.colorbar(label='Correlation Coefficient')
plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=90)
plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
plt.title("Correlation Matrix of Numeric Features")
plt.tight_layout()
plt.show()

# Identify top features correlated with wicket_next_over
target_corr = correlation_matrix['wicket_next_over'].drop('wicket_next_over').abs().sort_values(ascending=False)
print("Top features correlated with wicket_next_over:")
print(target_corr)

# Visualizing the distribution of a couple of important features:
# Let's pick, for example, 'dot_ball_pressure' and 'current_bowler_economy'

features_to_plot = ['dot_ball_pressure', 'current_bowler_economy']
for feature in features_to_plot:
    plt.figure(figsize=(8, 5))
    # Plot histogram for both classes of wicket_next_over
    for wicket_val in [0, 1]:
        subset = df[df['wicket_next_over'] == wicket_val]
        plt.hist(subset[feature], alpha=0.5, label=f'wicket_next_over = {wicket_val}', bins=15)
    plt.xlabel(feature)
    plt.ylabel("Frequency")
    plt.title(f"Distribution of {feature} by wicket_next_over")
    plt.legend()
    plt.show()
