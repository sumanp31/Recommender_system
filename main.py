import warnings
import numpy as np
import pandas as pd
from scipy.stats import mode
import time

warnings.filterwarnings("ignore", category=FutureWarning)

df = pd.read_csv("Merged_table.csv", nrows=1)
cols = df.columns
df = pd.read_csv("Merged_table.csv", usecols=cols[1:], nrows=5000)
df = df.loc[:, (df != 0).any(axis=0)]
userID = [x for x in df.columns if 'user' in x]
print (len(userID))
for usr in userID: ##Linear Regression for each user
	st = time.time()
	print (usr)
	userID1 = userID.copy()
	userID1.remove(usr)
	ids = list(df.columns)
	ids = [x for x in ids if (x not in userID1 and x not in 'name')]
	print (ids)
	df_new = df[ids]
	
	Y = df_new[usr].values
	ind = [x for x in range(len(df_new.index)) if Y[x] != 0]
	ind0 = [x for x in range(len(df_new.index)) if Y[x] == 0]
	
	ids.remove(usr)
	X = df_new[ids].values

	from sklearn.linear_model import LinearRegression

	linreg = LinearRegression() 
	linreg.fit(X[ind],Y[ind])
	Y[ind0]= linreg.predict(X[ind0])

	df[usr] = Y
	print("--- %s seconds ---" % (time.time() - st))


df.to_csv("filled_table.csv")

rec_d = pd.DataFrame()

## Create recommendation list

for usr in userID:
	d = df.nlargest(10, [usr])
	rec_d[usr] = d['name'].values

rec_d.to_csv('Recommendation List.csv')
