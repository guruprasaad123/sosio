import pandas as pd

df= pd.read_csv('stocks.csv',delimiter=",")

df= df.sort_values(by='date')

print(df.head(10))
print(df.tail(10))
