#
import pandas as pd
import numpy as np

dataset = pd.read_csv("cost_of_living_csv.csv")
#%%

#Get transpose of the dataset
data = dataset.transpose()

#Seperate city names 
cities = data.index.tolist()
cities.remove(cities[0]) 
cities_df = pd.DataFrame(cities, columns=['City'])

data.columns = data.iloc[0]
data = data[1:].reset_index(drop=True)

#Create new column
data["City"] = cities_df

df = data
#%%

#Move the City column to the 1st
cols = data.columns.tolist()
cols = cols[-1:] + cols[:-1]
data = data[cols]

#%%

#regular expressions library will be used to make some preprocessing operations
import re

#Delete "-Turkey" from City column
string = df["City"]
pattern = r"-Turkey"
replace = ""
df["City"] = df["City"].apply(lambda x: re.sub(pattern, replace, x))

#%%

# ".00 TL" delete the letters after "."
pattern = r"\.\d+\s*TL" 
replace = ""
df1 = df.map(lambda x: re.sub(pattern, replace, str(x)))

#Replace the "" instead of ","
df1 = df1.map(lambda x: x.replace(",",""))

#%%

#delete the "$" letter that in row 45
pattern = r"\s*\$"
replace = ""
dolar_in_TL = 34
df2 = df1.map(lambda x: re.sub(pattern, replace, str(x)))

#convert dollar value into Turkish Lira
df2.iloc[45, 1:-1] = df2.iloc[45, 1:-1].map(lambda x: float(x) * dolar_in_TL if x != "?" else x)

#Make it integer
df2.iloc[45, 1:-1] = df2.iloc[45, 1:-1].map(lambda x: int(x) if x != "?" else x)

#%%

#Make integer each non-null value between 1st and the last column
df2.iloc[:,1:-1] = df2.iloc[:,1:-1].map(lambda x: int(x) if x != "?" else x)

#Make the last column Float
df2.iloc[:,-1] = df2.iloc[:,-1].map(lambda x: float(x) if x != "?" else x)

#%%

#Replace the Nan instead of "?"
df2.replace("?", np.NaN, inplace = True)

#%%

#you can save by excel to the same folder

#df2.to_excel("preprocessed_data.xlsx",index=False)

df3 = df2.T