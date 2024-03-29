import pandas as pd

# Constant to multiply with
EXRate = pd.read_csv('DataTables\\EXRate.csv', index_col='Currency')
EXRate = EXRate['USD']['JPY']
print(EXRate)


df1 = pd.read_csv('DataTables\\tcgplayer.csv')


df2 = pd.read_csv('DataTables\\yuyutei.csv')

df2['price'] /= EXRate
df2['Currency'] = 'USD'

merged_df = pd.concat([df1, df2])

# Save the merged dataframe to a new CSV file
merged_df.to_csv('DataTables\\all_data.csv', index=False)  # 'index=False' to not write row indices
