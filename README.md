# Exploration of Trap and Dubstep through YouTube and Spotify Data - IT299 Project

A Python webscraping, data exploration, visualization, and dashboard hosting project.

## Introduction

This dashboard allows you to explore the electronic bass music genres of Trap and Dubstep through YouTube and Spotify data. 
Tracks related to these genres were gathered by scraping five popular music-discovering channels on YouTube: TrapNation, TrapCity, BassNation, UKFDubstep, and DubRebellion. 
Audio features data was tied to those that could be found in Spotify’s library. 

Link to the hosted dashboard is [here](https://trap-dash.herokuapp.com/).

## 1. Scrape

First scraped titles and IDs of all videos of relevant channels through YouTube's API and used [Pafy](https://pypi.org/project/pafy/) to extract individual video's metadata. Video titles had to be extracted and cleaned before passing into Spotify's API to search. The [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) library was used to match track names using the [Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance) method. If the match result did not pass a confidence threshold, the durations of the YouTube and Spotify tracks were compared to boost the level of confidence that the two tracks were the same. Finally, the Spotify ID of the matched track could then be used to query its [audio features](https://developer.spotify.com/documentation/web-api/reference/#object-audiofeaturesobject).

(See main.ipynb)

## 2. Store

Data was split into separate tables and stored in a PostgreSQL backend. Database entity relationship diagram below.
![alt text](https://github.com/jko0401/IT299-project/blob/main/ERD.PNG?raw=true)

(See db.ipynb)

## 3. Build

Dashboard was built using Plotly Dash, showcasing the following ways of exploring and visualizing data:

**Filters**:
Filter the dataset by artists or channels, and through different time ranges by YouTube publish or Spotify release dates. Data points can be differentiated by color through artists or channels.

**Feature Summary**:
Compare the mean, max, min of a specific feature for each artist.

**Compare Features**:
Compare any two features and see if there is a correlation between them.

**Feature Distributions**:
A set of histograms to help visualize the frequency and distribution of audio features pertaining to the tracks of the artists or channels selected. 

**Similar Tracks**:
Tracks that are similar in terms of their audio features are grouped together through [principal component analysis](https://en.wikipedia.org/wiki/Principal_component_analysis). The closer the tracks, the more similar they are.

**Selected Track**:
Preview any track through an embedded YouTube video.

(See app.py)

## 4. Host

Dashboard hosted on [Heroku](https://www.heroku.com/home) and data hosted on [ElephantSQL](https://www.elephantsql.com/).

## 5. Limitations
- The dataset does not automatically update. The most recent data was from the end of January when everything was scraped.
- Not all tracks uploaded to YouTube could be found on Spotify. Many SoundCloud-only tracks, unofficial releases, remixes that also represent the genres were not included in this dataset.
- Not all Spotify tracks of artists in this dataset were included, only those uploaded and shared by the five YouTube channels were selected.

## License
[MIT](https://choosealicense.com/licenses/mit/)
