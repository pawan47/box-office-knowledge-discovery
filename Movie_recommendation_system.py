import imp
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer as t
import numpy as np
import nltk
import pandas
import time


from nltk import tokenize,word_tokenize
from nltk.corpus import stopwords
import re
print('**-----------------Training--------------------**')

def create_soup(x):
	return ''.join(x['Description']) + '.' + ''.join(x['Storyline'])
 

def process_sentence(text,stem = False,lem = True,remove_stop_words = True,stemmer = nltk.PorterStemmer(),wnl = nltk.WordNetLemmatizer(),stop_word = stopwords.words('english') ):
	text = re.sub(r"[^A-Za-z0-9]"," ",text)
	text = re.sub(r"\'s","",text)
	text = re.sub(r"\'ve","have",text)
	text = re.sub(r"can't", "cannot ", text)
	text = re.sub(r"n't", " not ", text)
	text = re.sub(r"I'm", "I am", text)
	text = re.sub(r" m ", " am ", text)
	text = re.sub(r"\'re", " are ", text)
	text = re.sub(r"\'d", " would ", text)
	text = re.sub(r"\'ll", " will ", text)

	word = word_tokenize(text)
	
	if remove_stop_words:
		word = [wo for wo in word if not word in stop_word]
		
	if lem:
		word = [wnl.lemmatize(t) for t in word]
	
	if stem:
		word = [stemmer.stem(t) for t in word]
	return ' '.join(word)


def clean_data():
	for i in range(len(over_)):
		over_[i] = process_sentence(over_[i])



def suggest_movie(title):
	ind = indices[title]
	if type(ind) == pandas.core.series.Series:
		ind = ind.values[0] 
	txt = process_sentence(over[ind])
	#print(txt)
	vec = tfidf_vec.transform([txt])
	#print(vec.shape)
	ar = np.dot(vec,tf_idf_mat.T)
	ar =ar.toarray()
	ar = np.reshape(ar,ar.shape[1])
	ar = list(enumerate(ar))
	sim_scores = sorted(ar, key=lambda x: x[1], reverse=True)
	sim_scores = sim_scores[1:11]
	
	movie_indices = [i[0] for i in sim_scores]
	
	return data['Title'].iloc[movie_indices]


def pre_print(kk):
	kk = kk.values
	print()
	for i in range(len(kk)):
		print(i+1,kk[i])
	print()

data = pd.read_csv('Final_dataset.csv')
data.isna().sum()
data = data.fillna(' ')

data['soup'] = data.apply(create_soup, axis=1)

over = data['soup']
over_ = data['soup'].values

clean_data()

tfidf_vec = t()
tfidf_vec.fit(over_)
tf_idf_mat = tfidf_vec.transform(over_)

indices = pd.Series(data.index, index=data['Title']).drop_duplicates()


print('**-----Trained!!! Waiting for your input-------**')
while True:
	print('**---------------------------------------------**')
	print('press 1 to continue')
	print('press 2 to input mannual movie')
	print('press 3 to exit')
	print('**---------------------------------------------**')
	ino = int(input())
	take_screen_input = False
	take_random_movie = True
	if ino == 2:
		print('Please enter correct name')
		take_screen_input = True
		take_random_movie = False
	if ino == 1 or ino == 2:
		
		if take_screen_input:
			movie_ = str(input())
		elif take_random_movie:
			movie_ = data['Title'][np.random.randint(data.shape[0])]
		else:
			movie_ = 'The Godfather'
		print('')
		print('')
		print('Movie Recommendation for \"{}\"'.format(movie_))
		st = time.time()
		lll = suggest_movie(movie_)
		pre_print(lll)
		print('Time taken to suggest \"{}\" movie: {}'.format(movie_,time.time() - st))
		print('')
		print('')
	if ino ==3:
		print('*******Demo Ends Here*******')
		break
