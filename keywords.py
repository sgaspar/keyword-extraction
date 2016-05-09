
import six
import rake
import operator
import io
import os
import zipfile
import numpy as np
import re
import operator
import string
import csv
import logging
import time
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',\
    level=logging.INFO)

start_time = time.time()
print ('started at: ' + time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(start_time)))

# Grab files from a local directory and process each
files = os.listdir('epub-input/')
epubs = [x for x in files if '.epub' in x]
epubids = []

# Extracts books to a folder for use in a UI, if needed
for epub in epubs:
    bookid = re.sub(r'(.*).epub',r'\1',epub)
    epubids.append(bookid)
    # print 'extracting ' + bookid + '...'
    with zipfile.ZipFile('epub-input/' + str(epub),'r') as z:
        z.extractall('./www/epub-output/' + str(bookid))

log_time = time.time()
print ('books extracted at: ' + time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(log_time)))

bookids = []
filenames = []
chapters = []
locations = []
p_bookids = []
keywordlist=[]
rake_objects=[]

# Using rake stopwords list provided, would like to use nltk's stopword list 
# which seems better, then use rake.py and set recurrence, length and sentence criteria for evaluation
stoppath = "SmartStoplist.txt"
rake_object = rake.Rake(stoppath, 5, 3, 4)

# Get me the chapters of the book, then run them through the rake object to score the potential keywords
print ('gathering xhtml or html files...')
for root, dirs, files in os.walk('.'):
    for filename in files:
        if '.xhtml' in filename or '.html' in filename:
            full_filepath = root + '/' + filename
            bookid = re.sub(r'.*/epub-output/(.*?)/.*',r'\1',root)
            if bookid in epubids:
                bookids.append(bookid)
                filenames.append(filename)
                soup = BeautifulSoup(open(full_filepath), 'lxml')
                [s.extract() for s in soup('script', 'style', 'epub:switch')]
                filetext = soup.find('body').get_text()
                # Don't have to, but I kept chapters(filetext) and the keywords as seperate thigns so I can spit 
                # out into a single file if needed. Having some issues with encoding and special character handling with .csv
                chapters.append(filetext)
                keywords = rake_object.run(filetext)
                keywordlist.append(keywords)
                locations.append(filename)

num_chapters = len(chapters)

log_time = time.time()
print (str(len(chapters)) + ' chapters extracted at: ' + time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(log_time)))

# Write data to a .CSV for viewing, need to add encoding here to get rid of some special characters
with open('keyword-output/' + bookid + 'keyword_output.csv', 'w') as keyword_output:
    fieldnames = ['cluser', 'book', 'location', 'keywords']
    writer = csv.DictWriter(keyword_output, fieldnames=fieldnames, lineterminator=os.linesep)
    writer.writeheader()

    p_indices = []
    for i in range(0,num_chapters):
        p_indices.append(i)

    for p_index in p_indices:
            writer.writerow({'book': bookids[p_index], 'location': locations[p_index], 'keywords':keywordlist[p_index]})

# Tell me it's finished
end_time = time.time()
print ('finished outputting csv at: ' + time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(end_time)))
print ('total time elapsed: ' + str(end_time - start_time) + ' seconds.')
