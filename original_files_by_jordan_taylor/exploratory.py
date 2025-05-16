import pandas as pd

file_path = 'questions.csv'

df = pd.read_csv(file_path)

header = list(df.columns)
sample = df.head(5).values.tolist()
missing_rows = df[df.isnull().any(axis=1)].index.tolist()

print(f"Header: {header}")
print(f"Sample data: {sample}")
print(f"Rows with missing values: {missing_rows}")