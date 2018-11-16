Knowledge Discovery and Box Office Prediction of Movies
=======================================================

Course Project  
CS685A: Data Mining

Team
----

Ayush Anurag  
Dheeraj Athrey  
Pawan Agarwal  
Pawan Mishra  
Rohit Gupta  
Shivam Pal

Collaboration
------------

1. Clone and enter into the repository  
```
git clone https://github.com/pawan47/box-office-knowledge-discovery.git
cd path/to/cloned-directory
```

2. Team members should make changes and test their code in their specific branch  
Each branch should be named as *user-initials* followed by *working-branch*  
Example: for initials *XYZabc* typing `git checkout -b xyzabc-working-branch` will create and checkout into the *xyzabc-working-branch*  
Omit the `-b` flag if the branch already exists  
Do not make a new branch for everytime some code is to be added or modified

3. Access and upload data [here](https://drive.google.com/drive/folders/1uMUfso4577TO1RnfVHzqAg2oTW6XtWaS?usp=sharing)  

Goals
-----

1. Prepare of a consolidated database of movie details (cast,
director, production house, description, critical analysis, wikipedia) by
web-scraping

2. Preparing a ML model to predict movie ratings and Box-office
performance of the movies based on these factors

Pre-requisite:
--------------
Pakages used:
All codes are written in python3(>3.5). To install all dependency run the following command
```
pip install scrapy
pip install sklearn
pip install xgboost
pip install pandas
```

Data Collection
---------------

All the data used for recomendation and prediction has been collected from *IMDB* webpages of the movies. A automatic web scraping program has been implemented using the Scrapy framework, to perform data collection. To run the program follow the instructions below:

1. Install Scrapy: `pip install scrapy` or if you use anaconda, `conda install scrapy`

2. Clone the repository and enter into the **data-collection** folder of the repository  
```
git clone https://github.com/pawan47/box-office-knowledge-discovery.git
cd path/to/cloned-directory/data-collection
```

3. Enter `scrapy list` on the terminal to obtain the list of spider programs and related instructions.  
There are two spider programs: **imdbLinks** and **movieCrawler**  
**movieCrawler** is the main spider program and it can only be run after seed urls have been collected and saved. To obtain the seed urls run **imdbLinks** spider enter `scrapy crawl imdbLinks` in the terminal.  
This program will save a JSON file (**imdbLinks.json**) to links folders. This file contains a dictionary of links that will be used by the main spider program to crawl through the *IMDB* website.

4. To run the main spider program, enter `scrapy crawl movieScraper` in the terminal. This program will scrape the necessary information from *IMDB* movie pages and then follow the links on the page to other movie pages. All data of a particular movie is saved in a *JSON* file in the **movies** folder. No provision has been made in the program to automatically stop. Manually stop the program once enough data has been collected.

The collected raw data of about 50000 movies can be found in the data folder on drive.

### Method

The has been collected by recursively following links on movies pages of *IMDB* website. The starting urls are the links to *IMDB* top 250 movies. Patterns in the movie webpage have been identified and by element analysis of the pages, the necessary information has been picked. **xpath** has been used to pick information. Following information is collected for each movie (most of the fields are self-explanatory):

* Id: unique identification string for each movie
* Title
* Film_rating: who can watch the movie; PG-13, R and so on
* Duration
* Description
* IMDB_Rating
* IMDB_rating_count: number of people who have rated the movie
* Genre
* release_data
* Storyline
* Cast
* Taglines
* Director
* Writers
* Budget
* Revenue
* Country
* Language
* url

Each file is saved with *Id* as filename.
