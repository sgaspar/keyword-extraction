### ePub Keyword Extraction

#### Goals of this script
* Accept a directory of .epub books as input * Break epub into tokenized
chapters of content * Evaluated each chapter using RAKE (Rapid Automated
Keyword Extraction) to determine potential keywords and weighting

#### To run
* Import all modules, most importantly RAKE
(https://github.com/aneesha/RAKE) * Make sure you are in the right local
directory * Make keywords

#### To explore results
* Open keyword-output and open the .CSV(s) to review keywords for each
chapter
* Each line is a chapter file identified from the .ePub file, keywords are scored accordingly based on recurrence, size and placement around other non stopworkds

#### Conclusions
* At an initial pass RAKE does a great job of using keyword
identification theory to find things that "could" be keywords. More
often than not

#### What's Next
* Look at ways to limit the number of keywords per chapter, some of these chapters depending on who wrote said book use words too often that don't mean anything but could be construed as a keyword via the algoritm (see GREAT, SUPER when talking about themselves or their research. :-)
* * Using averages and the top half as a starting point then going from there
* Add in "sentiment" to determine user feedback to keywords identified (i.e. helpful/not helpful)
* Expose via public API endpoint for fun and since I love APIs.

#### Credits
Thanks to Nick Brown(https://github.com/uptownnickbrown) for the start on his ePub extraction tool made
this a couple hour project vs days.
