import pandas as pd
import numpy as np 
import os

data = pd.read_csv("Final_dataset.csv",low_memory=False)
k = 20
c = data['IMDB_rating'].mean()
m = data['IMDB_rating_count'].quantile(.9)
passed_movies = data.copy().loc[data['IMDB_rating_count']>=m]
v = passed_movies['IMDB_rating_count']
r = passed_movies['IMDB_rating']

score = ((2*v*r)/(v+m)) + ((m*c)/(v+m))

passed_movies['score']= score
passed_movies = passed_movies.sort_values('score',ascending=False)
pas = passed_movies['Title'].values
for i  in range(k):
	if i<9:
		print(i+1,'          ',pas[i])
	else:
		print(i+1,'         ',pas[i])
#print(passed_movies[['Title','IMDB_rating']].head(250))