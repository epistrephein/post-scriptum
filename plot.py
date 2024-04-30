"""Plot statiscal data from the linguistic analysis and save each graph as PNG."""

import json
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = 'static/plots'

######## 1. Zipf's Law ########
# Sample only the first 500 words to avoid making the graph unreadable
ALL_WORDS_SAMPLE = 500

with open('data/all_words.json', 'r', encoding='utf-8') as jsonfile:
    all_words = json.load(jsonfile)

x_axis = np.arange(ALL_WORDS_SAMPLE)
y_axis = list(all_words.values())[0:ALL_WORDS_SAMPLE]

plt.figure(figsize=(10, 8))
plt.plot(x_axis, y_axis, color='mediumblue') # https://matplotlib.org/stable/gallery/color/named_colors.html
plt.title("Zipf's law")
plt.xlabel("Word count")
plt.ylabel("Frequency")
plt.xticks(ticks=np.arange(0, ALL_WORDS_SAMPLE + 1, 50))

filename = f"{OUTPUT_DIR}/zipf.png"
plt.savefig(filename)
print(f'💾 Saved to {filename}')

######## 2. Most recurring nouns globally ########
with open('data/all_years-clean.json', 'r', encoding='utf-8') as jsonfile:
    all_years = json.load(jsonfile)

nouns = all_years['nouns']
x_axis = list(nouns.keys())
y_axis = list(nouns.values())

plt.figure(figsize=(10, 8))
plt.barh(x_axis, y_axis, color='dodgerblue')
plt.title('Most mentioned nouns (global)')
plt.xlabel('Frequency')

filename = f"{OUTPUT_DIR}/global-nouns.png"
plt.savefig(filename)
print(f'💾 Saved to {filename}')

######## 3. Most recurring verbs globally ########
verbs = all_years['verbs']
x_axis = list(verbs.keys())
y_axis = list(verbs.values())

plt.figure(figsize=(10, 8))
plt.barh(x_axis, y_axis, color='coral')
plt.title('Most mentioned verbs (global)')
plt.xlabel('Frequency')

filename = f"{OUTPUT_DIR}/global-verbs.png"
plt.savefig(filename)
print(f'💾 Saved to {filename}')

######## 4. Most recurring cities globally ########
cities = all_years['cities']
x_axis = list(cities.keys())
y_axis = list(cities.values())

plt.figure(figsize=(10, 8))
plt.barh(x_axis, y_axis, color='forestgreen')
plt.title('Most mentioned cities (global)')
plt.xlabel('Frequency')

filename = f"{OUTPUT_DIR}/global-cities.png"
plt.savefig(filename)
print(f'💾 Saved to {filename}')

######## 5. Most recurring nouns per year ########
with open('data/nouns_years-clean.json', 'r', encoding='utf-8') as jsonfile:
    nouns_years = json.load(jsonfile)

for year, data in nouns_years.items():
    x_axis = list(data.keys())
    y_axis = list(data.values())

    plt.figure(figsize=(10, 8))
    plt.barh(x_axis, y_axis, color='mediumorchid')
    plt.title(f'Frequency of nouns ({year})')
    plt.xlabel('Frequency')

    filename = f"{OUTPUT_DIR}/yearly-nouns-{year}.png"
    plt.savefig(filename)
    print(f'💾 Saved to {filename}')

######## 6. Follow the frequency of specific words across the years ########
with open('data/followed_words.json', 'r', encoding='utf-8') as jsonfile:
    followed_words = json.load(jsonfile)

for word, data in followed_words.items():
    x_axis = list(data.keys())
    y_axis = list(data.values())

    plt.figure(figsize=(10, 8))
    plt.plot(x_axis, y_axis, marker='o', color='red')
    plt.title(f'Followed word: {word}')
    plt.xlabel('Year')
    plt.ylabel('Frequency')

    filename = f"{OUTPUT_DIR}/followed-{word}.png"
    plt.savefig(filename)
    print(f'💾 Saved to {filename}')
