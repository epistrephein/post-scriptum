"""Perform a linguistic analysis of the dataset using a NLP model and save some statistics as JSONs."""

import os
import json
from collections import Counter
import spacy

DATASET_FILENAME = 'data/dataset.json'

MAX_YEAR = 2023
MIN_YEAR = 2018
POS_TAGS = ['NOUN', 'PROPN', 'VERB'] # https://spacy.io/usage/linguistic-features#pos-tagging
FOLLOW_WORDS = ['coronavirus', 'sciopero', 'incendio', 'scuola', 'carcere', 'terremoto', 'ndrangheta']

# Ensure the dataset file exists
if not os.path.exists(DATASET_FILENAME):
    print("❌ Dataset not found. Please run scrape.py first")
    exit()

# Load and parse the dataset
with open(DATASET_FILENAME, 'r', encoding='utf-8') as jsonfile:
    DATASET = json.load(jsonfile)

# Load the medium-sized Italian model
NLP = spacy.load("it_core_news_md")

# Initialize variables to store the results
all_words = []
all_years = {tag: [] for tag in POS_TAGS}
nouns_years = {year: [] for year in range(MIN_YEAR, MAX_YEAR + 1)}
followed_words = {word: {year: 0 for year in range(MIN_YEAR, MAX_YEAR + 1)} for word in FOLLOW_WORDS}

tokens_analyzed = 0

for entry in DATASET:
    # Parse the article text with the NLP model
    text = entry[1]
    doc = NLP(text)

    for token in doc:
        # Print some progress information
        tokens_analyzed += 1
        print('⏳️ Analyzed tokens:', tokens_analyzed, end='\r')

        # Add any non-punctuation token to the list of all words
        if not token.is_punct:
            all_words.append(str(token.lower_))

        # Add the lemma to the global list if it's an accepted POS tag
        if token.pos_ in POS_TAGS:
            all_years[token.pos_].append(str(token.lemma_))

        # Add the lemma to the year-specific list if it's a noun
        if token.pos_ == 'NOUN':
            year = int(entry[0][:4])
            nouns_years[year].append(str(token.lemma_))

        # Follow the usage of specific words across the years
        if token.lemma_ in FOLLOW_WORDS:
            year = int(entry[0][:4])
            followed_words[token.lemma_][year] += 1

# Print final tally of analyzed tokens
print('⏳️ Analyzed tokens:', tokens_analyzed)

# 1. Count all_words and save the result to JSON
all_words_counter = dict(Counter(all_words).most_common())
all_words_filename = 'data/all_words.json'

with open(all_words_filename, 'w', encoding='utf-8') as infile:
    json.dump(all_words_counter, infile, indent=4, ensure_ascii=False)

print(f'💾 Saved to {all_words_filename}')

# 2. Count each POS of all_years and save the result to JSON
all_years_counter = {}
all_years_filename = 'data/all_years.json'
for tag, values in all_years.items():
    all_years_counter[tag] = dict(Counter(values).most_common(500))

with open(all_years_filename, 'w', encoding='utf-8') as infile:
    json.dump(all_years_counter, infile, indent=4, ensure_ascii=False)

print(f'💾 Saved to {all_years_filename}')

# 3. Count each noun of nouns_years and save the result to JSON
nouns_years_counter = {}
nouns_years_filename = 'data/nouns_years.json'
for year, values in nouns_years.items():
    nouns_years_counter[year] = dict(Counter(values).most_common(500))

with open(nouns_years_filename, 'w', encoding='utf-8') as infile:
    json.dump(nouns_years_counter, infile, indent=4, ensure_ascii=False)

print(f'💾 Saved to {nouns_years_filename}')

# 4. Save the followed_words to JSON
followed_words_filename = 'data/followed_words.json'
with open(followed_words_filename, 'w', encoding='utf-8') as infile:
    json.dump(followed_words, infile, indent=4, ensure_ascii=False)

print(f'💾 Saved to {followed_words_filename}')
