import urllib2
import re
from bs4 import BeautifulSoup

def get_top_n(d, n):
	return list(sorted(d.items(), key = lambda x: x[1], reverse = True))[:n]

# Use Beautiful Soup to parse the transcript
soup = BeautifulSoup(urllib2.urlopen('http://www.theguardian.com/world/2013/aug/11/rudd-v-abbott-the-debate-in-full-transcript').read())

# Read in stop words
stop_words = set([line.strip() for line in open('stopwords.txt')])

# We store what each speaker said in a dictionary
speakers = {}

# Regex used to extract words
word_pattern = re.compile(r"\b\S+\b")

# Keep track of the current speaker
current_speaker = ''
for segment in soup.find('div', {'class': 'flexible-content-body'}).find_all('p'):
	# For each segment, if it is a new speaker, change speaker
	if segment.strong:
		# Speaker's name is wrapped in <strong></strong> tags
		current_speaker = segment.strong.contents[0].split()[-1]

		# What is said is actually in the second part
		content = segment.contents[1]
	else:
		# This is a continued paragraph, so what is said is in the first part
		content = segment.contents[0]

	# Get all the words used by the current speaker
	words = word_pattern.findall(content)

	# Clean out stop words and change words to lowercase
	cleaned_words = [w.lower() for w in words if w.lower() not in stop_words]

	# Add these words to the frequency dictionary for this speaker
	freq = speakers.get(current_speaker, {})
	for word in cleaned_words:
		freq[word] = freq.get(word, 0) + 1
	speakers[current_speaker] = freq

# Find the top words used
print get_top_n(speakers['ABBOTT'], 20)