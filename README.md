# social-media-viz

Social Media ILWC Visualization project

## Requirements

* Python 3.x
* Neo4J
* LIWC dataset
* NRC Emolex dataset
* NRC Sentiment dataset
* Twitter data

```
# Install required Python modules
pip install -r requirements.txt
python index.py

# Install required client side JS modules
npm install
npm start
```

## Ideas

Calculate the overlap between any features
* Threshold
* Boolean

Look at connections
* Geographically
* Temporally
* Mentions
* Direct replies
* Same hashtags

Hive plots?
Force layout networks?

## Presentation

Histograms
Chord graph

## Data format

Word Count	wordcount

### Summary Variable
Analytical Thinking	analytic
Clout	Clout
Authentic	Authentic
Emotional Tone	Tone

### Language Metrics
Words per sentence
Words >6 letters
Dictionary words	Dic

### Function Words	function
Total pronouns	pronoun
Personal pronouns	ppron
  1st pers singular
  1st pers plural
  2nd person	you
  3rd pers singular
  3rd pers plural
Impersonal pronouns	ipron
Articles	article
Prepositions	prep
Auxiliary verbs	auxverb
Common adverbs	adverb
Conjunctions	conj
Negations	negate

### Grammar Other
Regular verbs	verb
Adjectives	adj
Comparatives	compare
Interrogatives	interrog
Numbers	number
Quantifiers	quant

### Affect Words	affect
Positive emotion	posemo
Negative emotion	negemo
Anxiety	anx
Anger	anger
Sadness	sad

### Social Words	social
Family	family
Friends	friend
Female referents	female
Male referents	male

### Cognitive Processes
Insight	insight
Cause	cause
Discrepancies	discrep
Tentativeness	tentat
Certainty	certain
Differentiation

### Perpetual Processes	percept
Seeing	see
Hearing	hear
Feeling	feel

### Biological Processes	bio
Body	body
Health/illness	health
Sexuality	sexual
Ingesting	ingest

### Core Drives and Needs	drives
Affiliation	affiliation
Achievement	achieve
Power	 power
Reward focus	reward
Risk/prevention focus	risk

### Time Orientation
Past focus	focuspast
Present focus	focuspresent
Future focus	focusfuture

### Relativity	relativ
Motion	motion
Space	space
Time	time

### Personal Concerns
Work	work
Leisure	leisure
Home	home
Money	money
Religion	relig
Death	death

### Informal Speech	informal
Swear words	swear
Netspeak	netspeak
Assent	assent
Nonfluencies	nonfl
Fillers	filler
All Punctuation
Periods	Period
Commas	Comma
Colons	Colon
Semicolons	SemiC
Question marks	QMark
Exclamation marks	Exclam
Dashes	Dash
Quotation marks	Quote
Apostrophes	Apostro
Parentheses (pairs)	Parenth
Other punctuation	OtherP
