import pandas as pd
import numpy as np
import time

st = time.time()

artists= pd.read_csv("artists.csv")
col = artists.columns
artists= pd.read_csv("artists.csv", usecols=col[0:2])
artists.index = artists['id'].values
artists.drop('id',axis=1,inplace=True)

## Assigning tags as columns
tags = pd.read_csv('tags.csv')
tagIDlist = tags['tagID'].values
artists = pd.concat([artists,pd.DataFrame(columns=tagIDlist)])
artists[tagIDlist] = 0

user_taggedartists = pd.read_csv('user_taggedartists.csv', usecols=['userID', 'artistID','tagID'])
df =  user_taggedartists.groupby('artistID')['tagID'].apply(list)
## Assigning values to the tag columns
print (len(user_taggedartists['artistID'].unique()))
# print (user_taggedartists['artistID'].unique())
print("--- %s seconds ---" % (time.time() - st))

rows = list(set(artists.index).intersection(user_taggedartists['artistID'].unique()))
# print (len(rows))
temp = [(1 if t in df[u] else 0) for u in rows for t in tagIDlist]
artists.loc[rows,tagIDlist] = np.reshape(temp, (len(rows), len(tagIDlist)))
print("--- %s seconds ---" % (time.time() - st))


artists.columns = ['name'] + ["tag" + str(i)for i in artists.columns  if type(i) == int]

## Assigning users as columns

user_artists = pd.read_csv('user_artists.csv')
userIDlist = user_artists['userID'].unique()

artists = pd.concat([artists,pd.DataFrame(columns=userIDlist)])
artists[userIDlist] = 0

df2 = user_artists.groupby('artistID')['userID'].apply(list)
wt = user_artists.groupby('artistID')['weight'].apply(list)

rows2 = list(set(artists.index).intersection(user_artists['artistID'].unique()))
artists.loc[rows2,userIDlist] = (np.reshape([wt[u][df2[u].index(i)] if i in df2[u] else 0 for u in rows2 for i in userIDlist],(len(rows2),len(userIDlist))))

artists.columns = [('user' + str(artists.columns[i]) if type(artists.columns[i]) == int else artists.columns[i]) for i in range(len(artists.columns))]


print("--- %s seconds ---" % (time.time() - st))
artists.to_csv("Merged_table.csv")