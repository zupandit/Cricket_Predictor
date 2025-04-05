import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('over_features.csv')

# Engineering new features
df['pressure_index'] = df['dot_ball_pressure'] * df['required_desired_run_rate']
df['wicket_pressure'] = df['number_of_wickets_lost'] * df['required_desired_run_rate']
df['late_over_flag'] = (df['over'] > 15).astype(int)
df['bowler_pressure'] = df['current_bowler_economy'] * (df['bowler_wickets_in_match'] + 1)  # +1 to avoid zeros
df['aggressiveness_index'] = df['striker_strike_rate'] * (df['striker_boundaries_hit'] + 1)

# List of new features to visualize
new_features = ['pressure_index', 'wicket_pressure', 'late_over_flag', 'bowler_pressure', 'aggressiveness_index']

# Plot the distribution of each new feature by wicket_next_over, save and display the plot
for feature in new_features:
    fig, ax = plt.subplots(figsize=(8, 5))
    for wicket in [0, 1]:
        subset = df[df['wicket_next_over'] == wicket]
        ax.hist(subset[feature], alpha=0.5, label=f'wicket_next_over = {wicket}', bins=20)
    ax.set_xlabel(feature)
    ax.set_ylabel("Frequency")
    ax.set_title(f"Distribution of {feature} by wicket_next_over")
    ax.legend()
    
    # Save the plot to a file in the local directory
    filename = f"{feature}_distribution.png"
    fig.savefig(filename, bbox_inches='tight')
    
    # Open (display) the plot
    plt.show()
    plt.close(fig)
