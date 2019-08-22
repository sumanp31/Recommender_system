import pandas as pd

artists= pd.read_csv("artists.csv")
col = artists.columns
artists= pd.read_csv("artists.csv", usecols=col[0:2])
artists.columns = ['artistID', 'name']
artists.index = artists['artistID'].values
artists.drop('artistID',axis=1,inplace=True)


## Assigning tags as columns
tags = pd.read_csv('tags.csv')
tagIDlist = tags['tagID'].values

for i in tagIDlist:
	artists['tag' + str(i)] = 0

user_taggedartists = pd.read_csv('user_taggedartists.csv', usecols=['userID', 'artistID','tagID'])

## Assigning values to the tag columns
print (len(user_taggedartists['userID'].unique()))
for u in user_taggedartists['userID'].unique():
	print(u)
	temp = [x for x in user_taggedartists.index if user_taggedartists['userID'][x] == u]
	df = user_taggedartists.iloc[temp]
	gf = df.groupby('artistID')['tagID'].apply(list)

	for i in df['artistID'].unique():
		for j in range(len(gf[i])):
			artists['tag' + str(gf[i][j])][i] = 1


## Assigning users as columns

user_artists = pd.read_csv('user_artists.csv' )

userIDlist = user_artists['userID'].unique()


for i in userIDlist:
	artists['user' + str(i)] = 0

## Assigning values to the user columns
print (len(userIDlist))
for u in userIDlist:
	print (u)
	temp = [x for x in user_artists.index if user_artists['userID'][x] == u]
	for i in temp:
		artists['user' + str(u)][user_artists['artistID'][i]] = user_artists['weight'][i]

artists = artists.loc[:, (artists != 0).any(axis=0)]
print (artists)


artists.to_csv("Merged_table.csv")