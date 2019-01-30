import re
from nltk.corpus import stopwords
from unidecode import unidecode
from nltk.stem.snowball import EnglishStemmer
from collections import Counter
import sys

if len(sys.argv) < 2:
	print("--> You need to specify a filename! es. 'example.txt'")
	sys.exit()
elif len(sys.argv) > 2:
	print("--> This script doesn't take parameters")
	sys.exit()
	
script_name, file = sys.argv

def get_file_tokens(filename):
	tokens = []
	with open(filename) as f:
		for line in f:
			tokens += re.split('\W+', line)
	return tokens

def filter_words(words):
	return [w for w in words if len(w)>=3 and w not in STOPWORDS]

def normalize_words(words):
	return [unidecode(w.lower()) for w in words]
	
def stem_words(words):
	s = EnglishStemmer()
	return [s.stem(w) for w in words]

def get_stem_mapping(words):
	s = EnglishStemmer()
	mapping = {}
	for w in words:
		stemmed_w = s.stem(w)
		if stemmed_w not in mapping:
			mapping[stemmed_w] = Counter()
		mapping[stemmed_w].update([w])
	return mapping
	
def destem_words(stems, stem_mapping):
	return [stem_mapping[s].most_common(1)[0][0] for s in stems]
	
tokens = get_file_tokens(file)
STOPWORDS = set(stopwords.words('english'))
	
normalized = normalize_words(tokens)
filtered_t = filter_words(normalized)

stemmed = stem_words(filtered_t)
stem_mapping = get_stem_mapping(filtered_t)
destemmed = destem_words(stemmed, stem_mapping)

c = Counter(destemmed)
ten_most_common = c.most_common(10)
one_words_occurred = len([p[0] for p in c.items() if p[1]==1])

#print(c["hello"]) #"hello" occurrencies
for i in range(5):
	print(' ')
print('-- Number of words: ', len(c))
print('-- Total number of words: ', sum(c.values()))
print('-- The most common word is: ', c.most_common(10)[0][0])
print('-- Number of words that occur only onece: ', one_words_occurred)
print(' ')
print('-- List of then most common words:')
for word in ten_most_common:
	print(word)

for i in range(5):
	print(' ')

