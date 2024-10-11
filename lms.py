import pandas as pd
df = pd.read_csv('cleaned-data.csv')
def replace_zeros_with_mean(group):
    for col in group.columns:
        if pd.api.types.is_numeric_dtype(group[col]):
            group[col] = group[col].replace(0, group[col].mean())
    return group
df = df.groupby('countryName').apply(replace_zeros_with_mean)
df.to_csv('cleaned-data-mean-replaced.csv', index=False)
