import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv('Chase2515_Activity(June).csv')

# Print column names to verify
print("Column names:", df.columns)

# Strip any extra spaces from column names
df.columns = df.columns.str.strip()

# Print first few rows to inspect data
print(df.head())

# Convert 'Posting Date' to datetime format
if 'Posting Date' in df.columns:
    df['Posting Date'] = pd.to_datetime(df['Posting Date'], format='%m/%d/%Y', errors='coerce')

    # Calculate cumulative balance
    df['Balance'] = df['Balance'].astype(float)  # Ensure Balance column is in float format

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['Posting Date'], df['Balance'], marker='o')
    plt.title('Balance Over Time')
    plt.xlabel('Date')
    plt.ylabel('Balance')
    plt.grid(True)
    plt.show()
else:
    print("The 'Posting Date' column is missing from the DataFrame.")
