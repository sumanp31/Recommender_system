import warnings
import numpy as np
import pandas as pd
from scipy.stats import mode

warnings.filterwarnings("ignore", category=FutureWarning)

df = pd.read_csv("Merged_table.csv")
cols = df.columns
df = pd.read_csv("Merged_table.csv", usecols=cols[1:])

userID = [x for x in df.columns if 'user' in x]


for usr in userID: ##Linear Regression for each user

	userID1 = userID.copy()
	userID1.remove(usr)
	ids = list(df.columns)
	ids = [x for x in ids if (x not in userID1 and x not in 'name')]
	df_new = df[ids]
	
	Y = df_new[usr].values
	ind = [x for x in range(len(df_new.index)) if Y[x] != 0]
	ind0 = [x for x in range(len(df_new.index)) if Y[x] == 0]
	Y_train = Y[ind]
	Y_rec = Y[ind0]
	
	ids.remove(usr)
	X = df_new[ids].values
	X_train = X[ind]
	X_rec = X[ind0]
	
	from sklearn.linear_model import LinearRegression

	linreg = LinearRegression() 
	linreg.fit(X_train,Y_train)
	Y_rec= linreg.predict(X_rec)
	
	Y[ind0] = Y_rec
	df[usr] = Y


df.to_csv("filled_table.csv")

rec_d = pd.DataFrame()

## Create recommendation list

for usr in userID:
	d = df.nlargest(10, [usr])
	rec_d[usr] = d['name'].values

rec_d.to_csv('Recommendation List.csv')
