import pandas as pd
import numpy as np
import ast
from sklearn.preprocessing import MultiLabelBinarizer
import imp
from sklearn.feature_extraction.text import TfidfVectorizer as t
import nltk
import time
from nltk import tokenize,word_tokenize
from nltk.corpus import stopwords
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

#functions
def create_soup(x):
	return ''.join(x['Description']) + '.' + ''.join(x['Storyline']) + ''.join(x['Taglines'])

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

#read final data (uploaded by Pawan A.)
data = pd.read_csv('data.csv')
data = data.fillna(' ')

#merging description & story
data['soup'] = data.apply(create_soup, axis=1)
new_d = pd.concat([data['soup'],data['Genre']],axis=1)

#making 'genre' into a list
for i in range(0,len(new_d['Genre'])):
	new_d['Genre'][i] = ast.literal_eval(new_d['Genre'][i])

#dropping garbage
c=0
indexes = []
for i in range(len(new_d['Genre'])):
	#print(i,len(new_d['Genre'][i]))
	if(len(new_d['Genre'][i])==0):
		#new_d.drop(new_d.index[i],inplace=True)
		indexes.append(i)
		c=c+1
	elif(len(new_d['soup'][i])<=20):
		#new_d.drop(new_d.index[i],inplace=True)
		indexes.append(i)
		c=c+1


print("# of Pts. to Dropped ",c)    
new_d.drop(new_d.index[indexes],inplace=True)
#reset index
new_d.reset_index(inplace=True,drop=True)

print("# of data points ",new_d.shape)

#merging labels
#Dictionary for new labels
new_labels = {
        'Action':'Action', 'Adventure':'Adventure', 'Animation':'Animation/Fantasy', 'Biography':'Others',
        'Comedy':'Comedy', 'Crime':'Crime',
        'Documentary':'Others', 'Drama':'Drama', 'Family':'Drama', 'Fantasy':'Animation/Fantasy',
        'Film-Noir':'Others', 
        'History':'Others',
        'Horror':'Mystery/Horror/Thriller', 'Music':'Music', 'Musical':'Music', 'Mystery':'Mystery/Horror/Thriller',
        'News':'Others', 'Romance':'Romance',
        'Sci-Fi':'Sci-Fi', 'Short':'Others', 'Sport':'Others', 
        'Talk-Show':'Others', 'Thriller':'Mystery/Horror/Thriller',
        'War':'Others',
        'Western': 'Crime'
}

#merge labels 
for i in range(len(new_d['Genre'])):
	#print(new_d['Genre'][i])
	new_lab = []
	for j in range(len(new_d['Genre'][i])):
		#print(new_d['Genre'][i][j])
		new_lab.append(new_labels[new_d['Genre'][i][j]])
	new_d['Genre'][i] = list(set(new_lab))    

#encoding into 1/0's
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(new_d['Genre'])
print("Labels : ",mlb.classes_)

over = new_d['soup']
over_ = new_d['soup'].values

print("cleaning data...")
clean_data()

#counts of labels tocomment
counts = np.sum(y,axis=0)
print("-----Counts of Labels-----")
for i in range(0,11):
	print(mlb.classes_[i],"=",counts[i])

#tfidf
tfidf_vec = t()
tfidf_vec.fit(over_)
tf_idf_mat = tfidf_vec.transform(over_)

#test-train split
x_train, x_test, y_train, y_test = train_test_split(tf_idf_mat, y, test_size=0.30, random_state=42)

print("-------------------Training LinearSVC------------------------")
for i in range(0,11):
	ytr = y_train[:,i]
	yts = y_test[:,i]
	#print()
	clf = OneVsRestClassifier(LinearSVC(random_state=0)).fit(x_train, ytr)
	ypr = clf.predict(x_test)
	if(i+1 in list([1,2,4,9,10,11])):
		print(i+1,"\tFor Genre:\t",mlb.classes_[i],"\t\t Accuracy = ",accuracy_score(yts,ypr))
		continue
	if(i+1 in list([8])):
		print(i+1,"\tFor Genre:\t",mlb.classes_[i],"Accuracy = ",accuracy_score(yts,ypr))
		continue
	if(i+1 in list([3])):
		print(i+1,"\tFor Genre:\t",mlb.classes_[i],"\t Accuracy = ",accuracy_score(yts,ypr))
		continue
	print(i+1,"\tFor Genre:\t",mlb.classes_[i],"\t\t\t Accuracy = ",accuracy_score(yts,ypr))
print("-------------------------------------------------------------")

print("-------------------Training LogisticRegression---------------")
for i in range(0,11):
	ytr = y_train[:,i]
	yts = y_test[:,i]
	#print(i+1," For Genre:\t",mlb.classes_[i])
	clf = OneVsRestClassifier(LogisticRegression()).fit(x_train, ytr)
	ypr = clf.predict(x_test)
	if(i+1 in list([1,2,4,9,10,11])):
		print(i+1,"\tFor Genre:\t",mlb.classes_[i],"\t\t Accuracy = ",accuracy_score(yts,ypr))
		continue
	if(i+1 in list([8])):
		print(i+1,"\tFor Genre:\t",mlb.classes_[i],"Accuracy = ",accuracy_score(yts,ypr))
		continue
	if(i+1 in list([3])):
		print(i+1,"\tFor Genre:\t",mlb.classes_[i],"\t Accuracy = ",accuracy_score(yts,ypr))
		continue
	print(i+1,"\tFor Genre:\t",mlb.classes_[i],"\t\t\t Accuracy = ",accuracy_score(yts,ypr))
print("-------------------------------------------------------------")


print("-------------------Training BernoulliNB----------------------")
for i in range(0,11):
	ytr = y_train[:,i]
	yts = y_test[:,i]
	#print(i+1," For Genre:\t",mlb.classes_[i])
	clf = OneVsRestClassifier(BernoulliNB()).fit(x_train, ytr)
	ypr = clf.predict(x_test)
	if(i+1 in list([1,2,4,9,10,11])):
		print(i+1,"\tFor Genre:\t",mlb.classes_[i],"\t\t Accuracy = ",accuracy_score(yts,ypr))
		continue
	if(i+1 in list([8])):
		print(i+1,"\tFor Genre:\t",mlb.classes_[i],"Accuracy = ",accuracy_score(yts,ypr))
		continue
	if(i+1 in list([3])):
		print(i+1,"\tFor Genre:\t",mlb.classes_[i],"\t Accuracy = ",accuracy_score(yts,ypr))
		continue
	print(i+1,"\tFor Genre:\t",mlb.classes_[i],"\t\t\t Accuracy = ",accuracy_score(yts,ypr))
print("-------------------------------------------------------------")

print("-------------------Training MultinomialNB--------------------")
for i in range(0,11):
	ytr = y_train[:,i]
	yts = y_test[:,i]
	#print(i+1," For Genre:\t",mlb.classes_[i])
	clf = OneVsRestClassifier(MultinomialNB()).fit(x_train, ytr)
	ypr = clf.predict(x_test)
	if(i+1 in list([1,2,4,9,10,11])):
		print(i+1,"\tFor Genre:\t",mlb.classes_[i],"\t\t Accuracy = ",accuracy_score(yts,ypr))
		continue
	if(i+1 in list([8])):
		print(i+1,"\tFor Genre:\t",mlb.classes_[i],"Accuracy = ",accuracy_score(yts,ypr))
		continue
	if(i+1 in list([3])):
		print(i+1,"\tFor Genre:\t",mlb.classes_[i],"\t Accuracy = ",accuracy_score(yts,ypr))
		continue
	print(i+1,"\tFor Genre:\t",mlb.classes_[i],"\t\t\t Accuracy = ",accuracy_score(yts,ypr))
print("-------------------------------------------------------------")












