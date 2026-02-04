import pandas as pd

# Define the data from the table
data = {
    "Instance": [],
    "MILP Best": [],
    "MILP Avg": [],
    "IMA Best": [],
    "IMA Avg": [],


    "Gap": []
}

# Create the dataframe
df = pd.DataFrame(data)

# Calculate the best solution difference (IMA Best vs MILP Best)
df['Best Diff'] = abs(df['IMA Best'] - df['MILP Best']) / df['MILP Best'] * 100

# Calculate the average solution difference (IMA Avg vs MILP Avg)
df['Avg Diff'] = abs(df['IMA Avg'] - df['MILP Avg']) / df['MILP Avg'] * 100

# Calculate Gap difference (IMA Gap vs MILP Gap)
df['Gap Diff'] = abs(df['Gap'])  # Assuming MILP Gap is zero, only IMA gap value matters

# Compute Overall Performance Difference (based on the formula provided)
df['Overall Performance Diff'] = df['Best Diff'] + df['Avg Diff'] + df['Gap Diff']

# Calculate the average performance ratio (IMA Best / MILP Best)
df['Performance Ratio'] = df['IMA Best'] / df['MILP Best']

# Calculate Weighted Overall Score (using simple weights of 1 for each factor)
weighted_score = (df['Best Diff'] + df['Avg Diff'] + df['Gap Diff']).mean()

# Summarize the results
summary = {
    "Average Best Diff (%)": df['Best Diff'].mean(),
    "Average Avg Diff (%)": df['Avg Diff'].mean(),
    "Average Gap Diff": df['Gap Diff'].mean(),
    "Average Overall Performance Diff": df['Overall Performance Diff'].mean(),
    "Average Performance Ratio": df['Performance Ratio'].mean(),
    "Weighted Overall Score": weighted_score
}

print(summary)
