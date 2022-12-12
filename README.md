# Anime Rating Predictor
By Shaun Katanosaka, Nina Nguyen, Hin Yat Tsang

### Project Description
We make a dataset of animes and relevant information from myanimelist.net. Then we use machine learning to predict an upcoming/currently airing anime's myanimelist rating.
### Package Versions
  - mal-api 0.5.2
  - pandas 1.4.2
  - csv 1.0
  - numpy 1.21.5
  - matplotlib 3.5.1
  - sklearn 1.0.2
### Demo File Description
The demo file already outlines what each code cell does and why it's there.
First, we get our dataset. This can be done by running the make_csv function in getMalDatatset.py.

#### IMPORATANT
This function takes an EXTREMELY long time to run if you wish to get the data of all of the anime on myanimelist.net. Instead, I recommend using the AnimeList.csv file provided in AnimeList.zip. If you wish to test out this function, then i recommend the following aruments:
make_csv(1, 20, 1, True, .5)

make_csv takes in up to 6 arguments: filename, minIndex, maxIndex, updates, progress_updates, progress_increment
- filename is a string storing the name of the file which will be created and written to. This string must end in .csv for the final product to be a .csv file.
- minIndex and maxIndex are ints which indicate the min and max ID values to iterate through and print into our .csv file.
- updates is an int, indicating the number of times our function will write to the .csv file. This int gives us an option to physically see our .csv file being made and updated, so that we know if something is going wrong quickly. This is important because this function runs extremely slowly.
- progress_updates is a bool, indicates whether or not to print how far along an update our function is.
- progress_increment is a float 0<x<1, which will display the percentage of completion our function is per update progress_increment times



Next, we read our .csv file into a pandas dataset and hand that into the AnimePredictor object as a parameter. The AnimePredictor class has many functions for data treating, making the predictive models, and getting our final result.

Now we run the AnimePredictor.treatData() and animeData.createModelVariables() methods to get our data ready to be used in our machine learning models.


Here is a distribution graph of the features to be used in the model.
![image](https://user-images.githubusercontent.com/117700006/206916321-bbeedbde-17af-45b4-96f0-cea242b681a6.png)



And here is a distribution graph of our label.


![image](https://user-images.githubusercontent.com/117700006/206916611-4a527bf8-0544-4c13-9416-62df400a06ba.png)



To get a prediction score, we first get the ID number of an anime from myanimelist.net. For example, the anime "Blue Lock" has a url "https://myanimelist.net/anime/49596/Blue_Lock", so the Id number for this anime is 49596. 

Then, we get our predicted scores by running AnimePredictor.printScoreTree(IDnumber) or AnimePredictor.printScoreLinearRegression(IDnumber).

Thse functions will print out the predicted score via decision tree regression or linear regression respectively.

One can also imput a list of ID numbers as a list of ints into these functions as well.

For example, AnimePredictor.printScoreTree([42962, 49979, 51212, 52046])  This will print out the predicted scores of all the animes in the list.


The class also stores the error scores, which can be accessed via AnimePredictor.T_score or AnimePredictor.lr_score.



To test our results, here is a graph comparing the model's results to the actual rating.
![image](https://user-images.githubusercontent.com/117700006/206916900-7462e469-8295-412d-bc99-a9d016fb9eb2.png)


Surprisingly, the model is pretty accurate for both models, despite the vastly different error scores.



### Scope, Limitations and Ethical Implications
- The make_csv function runs quite slowly, taking over 12 hours for the function to finish. If you wish to create a .csv file covering the entirety of myanimelist.net's database, I suggest running this program over a day.
- While this project's intended use is to predict an anime's score and potentially see whether an upcoming anime is worth watching or not, enjoyment is subjective and should not be used as an objective determination of how much one will enjoy the series.
- This program can only be used for animes which are either upcoming or currently airing(but not complete).

### Ideas for Potential Extensions
- Include more features into our model, such as genres, source material's rating(if applicable), animation studio, etc
- Add support for movie rating predictions

### References

https://myanimelist.net   The site which we gathered data from

https://mal-api.readthedocs.io/en/latest/index.html  The package we used to gather data from myanimelist.net 


https://www.pythontutorial.net/python-basics/python-write-csv-file/   The tutorial we used to learn how to write a csv file in python



### Demo Video
https://youtu.be/ZbeNkWy8enU
