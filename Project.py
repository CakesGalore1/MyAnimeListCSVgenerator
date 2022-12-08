import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from sklearn import tree
from sklearn import preprocessing


animes = pd.read_csv("AnimeCombineList.csv")
#creates the "y"
y = animes["score"]
X = animes.drop(["score"], axis = 1)

#drop categories that don't seem usefl towards our model
X = X.drop(["title","title_english","title_japanese","title_synonyms","url","image_url","rank","related_anime","opening_themes" ,"ending_themes" ,"characters", "staff","synopsis", "background", "ID"], axis = 1)

#drop more categories
categories_to_drop = ["genres", "themes", "aired", "premiered", "broadcast", "producers", "licensors", "studios", "source", "duration", "rating"]
X = X.drop(categories_to_drop, axis=1)

# Drop movies without a rating


#Drops any type belongs to ["Music", "Special", "ONA", "OVA", ""]
movie = X["type"] == "Movie"
TV = X["type"] == "TV"
X = X[movie | TV]



# makes an instance of labelencoder
le = preprocessing.LabelEncoder() 

#renames the status of "currently airing" or "finished airing" to 0 or 1 respectively
X["premiered"] = le.fit_transform(X["premiered"]) 

#renames the status of "TV" or "Movie" to 0 or 1 respectively
X["type"] = le.fit_transform(X['type']) 
np.unique(X["type"])
X = X[X["type"] != 2]

def makeModel(X,y):
    T = tree.DecisionTreeClassifier(max_depth=2) 
    T.fit(X, y) 


#makeModel(X,y)
X

le.inverse_transform([0,1])
