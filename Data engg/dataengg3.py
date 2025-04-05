import pandas as pd
import matplotlib.pyplot as plt
import itertools
import numpy as np

# Load the dataset
df = pd.read_csv('over_features.csv')

# Choose features to investigate
features = ['over', 'number_of_wickets_lost', 'required_desired_run_rate', 'dot_ball_pressure']

# Iterate over each pair of features and create hexbin plots for each wicket outcome
for feat1, feat2 in itertools.combinations(features, 2):
    fig, ax = plt.subplots(1, 2, figsize=(14, 6), sharex=True, sharey=True)
    
    # Create a hexbin plot for each class (wicket_next_over = 0 and 1)
    for i, wicket in enumerate([0, 1]):
        subset = df[df['wicket_next_over'] == wicket]
        hb = ax[i].hexbin(subset[feat1], subset[feat2], gridsize=30, mincnt=1, 
                          cmap='viridis', bins='log')
        ax[i].set_title(f"wicket_next_over = {wicket}")
        ax[i].set_xlabel(feat1)
        ax[i].set_ylabel(feat2)
        cb = fig.colorbar(hb, ax=ax[i])
        cb.set_label('log(count)')
    
    plt.suptitle(f"Hexbin Plots: {feat1} vs {feat2}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
