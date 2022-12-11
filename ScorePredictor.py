import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from sklearn import tree
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
pd.options.mode.chained_assignment = None

#class which takes in a dataset and can treat our data and make a model , and run a prediction
class AnimePredictor:
    """

    """
    def __init__(self, animes):
        """
        
        """
        self.animes = animes
        self.X = self.animes
        self.y = self.X
        self.X_train = self.X
        self.y_train = self.y
        self.X_test = self.X
        self.y_test = self.y
        self.T_score = 0
        self.lr_score = 0
    
    def removeScores(self):
        """
        #drop animes which do not have a score yet
        """
        self.animes = self.animes[self.animes["score"].notna()]
        self.animes = self.animes[self.animes["score"] != None]
        self.X = self.animes
        
    def removeCategories(self):
        """

        """
        #drop categories that don't seem useful towards our model
        self.X = self.X.drop(["title","title_english","title_japanese","title_synonyms","url","image_url","rank","related_anime",
                    "opening_themes" ,"ending_themes" ,"characters", "staff","synopsis", "background", "ID"], axis = 1)

        #drop more categories
        categories_to_drop = ["genres", "themes", "aired", "broadcast", "producers", "licensors", "studios", "source", "duration", "rating"]
        self.X = self.X.drop(categories_to_drop, axis=1)

    def removeUnnecessaryTypes(self):
        #not in ["Music", "Special", "ONA", "OVA", ""]
        self.X = self.X[self.X["type"] != "Music"]
        self.X = self.X[self.X["type"] != "Special"]
        self.X = self.X[self.X["type"] != "ONA"]
        self.X = self.X[self.X["type"] != "OVA"]
        self.X = self.X[self.X["type"] != ""]

    def removeUnnecessaryPremiered(self):
        """
        #get rid of animes which do not have a listed premiered season
        #virtually all of these are not TV series anyway
        """
        self.X = self.X[self.X["premiered"].notna()]
        self.X = self.X[self.X["premiered"] != None]
        self.X = self.X[self.X["premiered"] != "?"]

    
    def premieredToFloat(self, anime):
        """
        #converts "season" category to a numerical value
        """
        X = anime
        X[['season', 'year']] = X['premiered'].str.split(expand=True)
        X['season'] = X['season'].replace({"Winter": "0"})
        X['season'] = X['season'].replace({"Spring": "25"})
        X['season'] = X['season'].replace({"Summer": "50"})
        X['season'] = X['season'].replace({"Fall": "75"})
        X["new_premiered"] = (X["year"] + "." + X["season"]).astype("str")
        X["new_premiered"] = X["new_premiered"].astype(float)
        X.drop('year', inplace=True, axis=1)
        X.drop('season', inplace=True, axis=1)
        X = X.drop(["premiered"], axis = 1)
        X["premiered"] = X["new_premiered"]
        X = X.drop(["new_premiered"], axis = 1)
        return X
    
    def removeUnnecessaryStatuses(self):
        """
        
        """
        # makes an instance of labelencoder
        le = preprocessing.LabelEncoder() 

        #makes type into a number
        self.X["type"] = le.fit_transform(self.X['type']) 
        np.unique(self.X["type"])
        self.X = self.X[self.X["type"] != 2]

        #drop animes which are not finished airing(i.e. currently airing)
        self.X = self.X[self.X["status"] != "Currently Airing"]

        #drop the status category because they are all 
        self.X = self.X.drop(["status"], axis = 1)

        #drop the type category because all animes in our dataset at this point are all the same type(TV series)
        self.X= self.X.drop(["type"], axis = 1)

    def treatData(self):
        """
        
        """
        self.removeScores()
        self.removeCategories()
        self.removeUnnecessaryTypes()
        self.removeUnnecessaryPremiered()
        self.X = self.premieredToFloat(self.X)
        self.removeUnnecessaryStatuses()
    
    def createModelVariables(self):
        """
        makes self.y as our target variable
        """
        self.y = self.X["score"]
        #removes our target variable "score" from 
        self.X = self.X.drop(["score"], axis = 1)


    def fit_tree(self, X_train, y_train, d):
        """
        
        """
        T = tree.DecisionTreeRegressor(max_depth=d)
        T.fit(X_train, y_train)
        return T

    def predictScoreTree(self, animeID):
        """
        
        """
        if animeID in self.animes["ID"]:
            raise ValueError("animeID is not the ID to any anime in self.animes")
        anime = self.animes.loc[self.animes[self.animes["ID"]==animeID].index]
        anime = self.premieredToFloat(anime[list(self.X.columns)])
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3)
        animeScoreList = []
        errorScoreList = []
        for i in range(8):
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3)
            depths = range(1, 30)
            cv_scores = []
            for d in depths:
                T = self.fit_tree(self.X_train, self.y_train, d)
                cv_score = cross_val_score(T, self.X_train, self.y_train, cv=3).mean()
                cv_scores.append(cv_score)
            min_arg = np.argmax(cv_scores)
            self.fit_tree(self.X, self.y, depths[min_arg])
            animeScoreList.append(T.predict(anime))
            avgScore = np.round(np.mean(animeScoreList),2)
            errorScoreList = T.score(self.X,self.y)
        self.T_score = np.mean(errorScoreList)
        return avgScore
    
    def printScoreTree(self, animeID):
        """
        
        """
        if isinstance(animeID, int):
            animeID = [animeID]
        scores = []
        for i in animeID:
            if isinstance(i, int) == False:
                raise ValueError("animeID must be an int or list of ints")
            score = self.predictScoreTree(i)
            scores.append(score)
            print("The predicted score for \033[1;3m{0}\033[0m via Decision Tree Regressor is \033[1;3m{1}\033[0m".format(self.animes.loc[self.animes[self.animes["ID"]==i].index].iloc[0][1],score))
        return scores

    def predictScoreLinearRegression(self, animeID):
        """
        
        """
        if animeID in self.animes["ID"]:
            raise ValueError("animeID is not the ID to any anime in self.animes")
        lr = LinearRegression() 
        lr.fit(self.X, self.y)
        anime = self.animes.loc[self.animes[self.animes["ID"]==animeID].index]
        anime = self.premieredToFloat(anime[list(self.X.columns)])
        self.lr_score =  lr.score(self.X,self.y)
        return np.round(lr.predict(anime),2)[0]
    
    def printScoreLinearRegression(self, animeID):
        if isinstance(animeID, int):
            animeID = [animeID]
        scores = []
        for i in animeID:
            if isinstance(i, int) == False:
                raise ValueError("animeID must be an int or list of ints")
            score = self.predictScoreLinearRegression(i)
            scores.append(score)
            print("The predicted score for \033[1;3m{0}\033[0m via Linear Regression is \033[1;3m{1}\033[0m".format(self.animes.loc[self.animes[self.animes["ID"]==i].index].iloc[0][1], score))
        return scores
