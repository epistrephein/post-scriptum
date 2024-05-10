# Post Scriptum

Linguistic analysis Python app for the italian online newspaper Il Post.

## Description

The aim of the project is to perform a linguistic analysis on the articles of the online newspaper Il Post and visualize the results with some graphs on a Flask web application.
We start by scraping the articles from the website using the `requests` and `BeautifulSoup` libraries and persiting the dataset to JSON.  
Then we perform the linguistic analysis using the `spaCy` library, which includes tokenization, lemmatization, part-of-speech tagging and named entity recognition.
Finally, we generate some graphs using the `matplotlib` library to visualize the results.

## Usage

The project is a Flask web application that displays 4 linguistic analyses with some graphs and comments.

To run the project, first install the dependencies

```
pip install -r requirements.txt
```

then launch the Flask server

```
python web.py
```

and visit http://localhost:3000/ to view the website.
NOTE: The website runs on port 3000 instead of default 5000 because on macOS it is used
by internal utilities and [cause conflicts when the server is not running](https://stackoverflow.com/a/72797062).

### Python files involved

All the data and graphs that constitutes the analyses are already present in the repository, but can be regenerated using the scripts included.

1. `scrape.py` scrapes the articles from the website and saves them in the JSON file `data/dataset.json`.

```
python scrape.py
```

2. `analyze.py` reads the JSON file and performs the linguistic analyses, saving the results in different JSON files in the `data` folder.  
In the final project, the data has been manually cleaned to be more usable. These cleaned files can be identified by the `-clean` suffix.

```
python analyze.py
```

3. `plot.py` reads the JSON files created  and generates the graphs PNG files in the `static/plots` folder.

```
python plot.py
```

4. Finally, `web.py` is the Flask web application that displays the html pages with analyses and graphs.

```
python web.py
```
