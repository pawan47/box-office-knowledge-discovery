import warnings
warnings.filterwarnings("ignore")
import imp
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb

# these are encoded film rating
film_rating_encoding = {'Not Rated': 0, 'nan': 0, 'Unrated': 0, 'TV-G': 0, 'G': 0, 'Approved': 0, 'TV-PG': 1, 'Passed': 0, 'TV-14': 1, 'PG': 1, 'PG-13': 1, 'U': 0, 'GP': 1, 'M/PG': 1, 'R': 1, 'M': 1, 'TV-MA': 1, 'TV-13': 1, 'X': 1, 'NC-17': 1, 'A': 1, 'AO': 1, 'TV-Y7': 0, 'UA': 0, 'TV-Y': 0, '(Banned)': 1, 'Open': 1}


# data reading from imdb_data.csv
data = pd.read_csv("imdb_data.csv")


# extrsction of useful features from data
data_required = data[['Film_rating', 'Duration', 'IMDB_rating', 'IMDB_rating_count', 'release_date','Budget', 'Revenue', 'Country']]


# removal of junk values from data and from all features
data_required['film_rating'] = data_required.Film_rating.apply(lambda x: 0 if pd.isna(x) else film_rating_encoding[x])
data_required['duration'] = data_required.Duration.apply(lambda x: x if len(str(x))<4 else np.NaN)
data_required['release_year'] = data_required.release_date.apply(lambda x: str(x).split("-")[0]  if len(str(x))==10 else np.NaN)
data_required['budget'] = data_required.Budget.apply(lambda x: x if str(x)!="0" else np.NaN)
data_required['revenue'] = data_required.Revenue.apply(lambda x: x if str(x)!="0" else np.NaN)
data_required = (data_required.drop(['Film_rating', 'Duration', 'release_date', 'Budget', 'Revenue'], axis = 1)).dropna()
data_required.reset_index(inplace=True, drop = True)


# converting data into integer
data_required['revenue'] = data_required.revenue.apply(lambda x: int(x))
data_required['budget'] = data_required.budget.apply(lambda x: int(x))
data_required['release_year'] = data_required.release_year.apply(lambda x: int(x))
data_required['duration'] = data_required.duration.apply(lambda x: int(x))

data_required['IMDB_rating'] = data_required.IMDB_rating.apply(lambda x: float(x))
data_required['IMDB_rating_count'] = data_required.IMDB_rating_count.apply(lambda x: int(x))


# calculation of success column
revenue = np.array(list(data_required.revenue))
budget = np.array(list(data_required.budget))
profit = revenue - budget
success = []
for i in range(len(profit)):
    temp = profit[i]/float(budget[i])
    success.append(temp)
data_required['success'] = success


# normalisation of release year
min_year = data_required.release_year.min()
data_required['release_year'] = data_required.release_year.apply(lambda x: x - min_year + 1)


# calculation of country column
all_countries = []
country_list = list(data_required.Country)
for x in country_list:
    temp = x.split("\'")
    all_countries.append(temp[1])
data_required['country'] = all_countries


# country encoding
unique_countries = list(data_required.country.unique())
country_encoding = {}
c = 0
for x in unique_countries:
    country_encoding[x] = c
    c+=1
data_required['country_enc'] = data_required.country.apply(lambda x: country_encoding[x])


# calculation of score column
c = data_required.IMDB_rating.mean()
m = data_required.IMDB_rating_count.quantile(0.9)
v = data_required.IMDB_rating_count
r = data_required.IMDB_rating
score = ((2*v*r)/(v+m)) + ((m*c)/(v+m))
data_required['score'] = score

# final data
final_data = data_required[['film_rating', 'duration', 'release_year', 'score', 'country_enc', 'success','IMDB_rating','IMDB_rating_count']]
final_data.to_csv("final_data.csv", index = False)

data= pd.read_csv('final_data.csv')

nor = MinMaxScaler()
nor1 = MinMaxScaler()

x = nor.fit_transform(data.iloc[:,:-1])
y = nor.fit_transform(data.iloc[:,-1:])

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = .10)

pa = {
    'max_depth': 9,  # the maximum depth of each tree
    # eta': 0.5,  # the training step for each iteration
    'silent': 1} 

tr = xgb.DMatrix(x_train,y_train)
te = xgb.DMatrix(x_test,y_test)

reg = xgb.train(params=pa,dtrain=tr,num_boost_round=50)

polo = np.sqrt(((reg.predict(te) - y_test.T)**2).sum()/(len(y_test)))
print('**-------------Test Accuracy-----------------**')
print(polo)
print('**-------------------------------------------**')
