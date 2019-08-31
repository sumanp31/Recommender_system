# Recommender_system

Attempt at implementing a few recommendation algorithms and  try to build an ensemble of these models to come up with our final recommendation system

Due to the huge size of the data, I got a memoryerror and hence, I have run the linear regression only for first 5000 artists. In case your system has a memory greater than 8GB RAM, you can make the following change:
``` 
df = pd.read_csv("Merged_table.csv", usecols=cols[1:])
``` 
in the file ```main.py``` in line number **11** to run it for the entire artists list.