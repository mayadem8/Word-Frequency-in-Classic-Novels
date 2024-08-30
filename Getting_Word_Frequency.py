import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')
from nltk.probability import FreqDist
import string
import contractions
import csv
import re


headers = "Mozilla/5.0 (Windows NT 10.3; Win64; x64; en-US) AppleWebKit/601.29 (KHTML, like Gecko) Chrome/55.0.1010.318 Safari/603.1 Edge/16.37345"


url = "https://www.gutenberg.org/cache/epub/35688/pg35688-images.html"
response = requests.get(url, headers)
soup = BeautifulSoup(response.text, "lxml")
data = soup.find_all("p", attrs={"class": "dent"})


f = open("Alice_in_the_Wonderland.txt", "w")
for row in data:
    f.write(row.text)
f.close()

f = open("Alice_in_the_Wonderland.txt", "r")
lines = f.readlines()



all_tokens = []


for line in lines:
    expanded_line = contractions.fix(line)
    word_tokens = nltk.word_tokenize(expanded_line)
    for token in word_tokens:
        token = token.lower()
        if token not in string.punctuation:
            all_tokens.append(token)
    


with open("For_cleaning.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in all_tokens:
        writer.writerow([row])


with open("For_cleaning.csv", mode='r', newline='') as file1:
    reader = csv.reader(file1)
    Cleaned_data = []
    for row in reader:
        for item in row:
            if item in ['"', "'", '“', '”', '‘', '’']:  
                continue
            if len(item) < 2 and item not in ["a", "i"]:
                continue
            item = item.replace('—', '-')
            parts = re.split(r'[.-]', item)
            Cleaned_data.extend(part.strip() for part in parts)


with open("Cleaned.csv", mode='w', newline='') as file2:
    writer = csv.writer(file2)
    for item in Cleaned_data:
        writer.writerow([item.strip()])

all_words = []

file2 = open("Cleaned.csv", "r")
cleaned_lines = file2.readlines()
for line in cleaned_lines:
    line = line.replace('\n',"")
    all_words.append(line)


freq = FreqDist(all_words)


with open("Word_Frequencies.csv", mode='w', newline='') as file3:
    writer = csv.writer(file3)
    writer.writerow(['Word', 'Frequency'])
    writer.writerows(freq.most_common())

