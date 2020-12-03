import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data #✅
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column #✅
df1 = df[["weight", "height"]]
df["bmi"] = df["weight"] / ((df["height"] / 100 ) ** 2)
df['overweight'] = df['bmi'].apply(lambda x: 1 if x > 25 else 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df["cholesterol"] = df["cholesterol"].apply(lambda x: 1 if x > 1 else 0) #✅
df["gluc"] = df["gluc"].apply(lambda x: 1 if x > 1 else 0)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, value_vars=["active", "alco", "cholesterol", "gluc", "overweight", "smoke"], id_vars="cardio")


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat["total"] = 1

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(
        data = df_cat,
        col = "cardio",
        kind = "bar",
        x = "variable",
        y = "total",
        hue = "value").fig



    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data

    pressure_filter = df["ap_lo"] <= df["ap_hi"]
    height_filter = (df["height"] >= df["height"].quantile(0.025)) & (df["height"] <= df["height"].quantile(0.975))
    weight_filter = (df["weight"] >= df["weight"].quantile(0.025)) & (df["weight"] <= df["weight"].quantile(0.975))

    df_heat = df[pressure_filter & height_filter & weight_filter]
    df_heat = df_heat.drop('bmi',axis=1)

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(
        corr,
        mask = mask,
        linewidths = 0.5,
        annot = True,            
        fmt = ".1f",             
        center = 0.08,
        cbar_kws = {
            "shrink": 0.5       
        }
    )



    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
