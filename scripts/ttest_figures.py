# Create figures for the t-test analyses
# Claude.ai was used as help in the creation of this script

import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned dataset
data = pd.read_csv("../data/bright_light_data_clean.csv")

# Use the existing group colours
colours = {
    "Control_group": "#0c5ad7",
    "Light_group": "#f3be00"
}

# Create the figures folder if needed
import os
os.makedirs("../figures/t_tests", exist_ok=True)


# Create figures for each brain region
for region in ["Hippocampal_volume", "Amygdala_volume"]:

    # Set readable names for the graph labels
    if region == "Hippocampal_volume":
        region_name = "Hippocampal"
    else:
        region_name = "Amygdala"

    baseline = region + "_baseline"
    post = region + "_post"
    change = region_name + "_change"

    # Calculate change from baseline to post-treatment
    data[change] = data[post] - data[baseline]

    # Figure 1: Baseline vs. post-treatment
    plt.figure(figsize=(7, 5))

    for group, group_data in data.groupby("Group"):

        # Connect each participant's measurements
        for _, participant in group_data.iterrows():
            plt.plot(
                ["Baseline", "Post-treatment"],
                [participant[baseline], participant[post]],
                color=colours[group],
                alpha=0.35
            )

        # Show the group averages
        means = group_data[[baseline, post]].mean()
        plt.plot(
            ["Baseline", "Post-treatment"],
            means.values,
            color=colours[group],
            linewidth=3,
            marker="o",
            label=group
        )

    plt.xlabel("Time")
    plt.ylabel("Volume (mm$^3$)")
    plt.title(region_name + " volume: baseline vs. post-treatment")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        "../figures/t_tests/" + region_name.lower() + "_volume_over_time.png",
        dpi=300
    )
    plt.show()


    # Figure 2: Change in volume by group
    plt.figure(figsize=(7, 5))

    groups = ["Control_group", "Light_group"]
    values = [
        data.loc[data["Group"] == group, change].values
        for group in groups
    ]

    plt.boxplot(values, tick_labels=groups)

    # Show individual participants
    for i, group in enumerate(groups, start=1):
        group_data = data[data["Group"] == group]

        plt.scatter(
            [i] * len(group_data),
            group_data[change],
            color=colours[group],
            alpha=0.7
        )
    plt.axhline(0, color="grey", linestyle="--", linewidth=1)
    plt.xlabel("Group")
    plt.ylabel("Change in brain volume (post - baseline)")
    plt.title(region_name + " volume change by group")
    plt.tight_layout()
    plt.savefig(
        "../figures/t_tests/" + region_name.lower() + "_volume_change_boxplot.png",
        dpi=300
    )
    plt.show()

print("All four figures have been saved in the figures folder.")