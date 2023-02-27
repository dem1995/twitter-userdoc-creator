# twitter-userdoc-creator
Creates user documents when provided a collection of Tweets in .jsonl format

## Usage
Takes in a .jsonl file of tweets and spits out a series of .jsonol files of
tweets, one file per Twitter user.
```
positional arguments:
  input                 The .jsonl tweet files to take in to produce user
                        documents from

options:
  -h, --help            show this help message and exit
  -o [OUTDIR], --outdir [OUTDIR]
                        The directory to output the tweet files to. Defaults
                        to 'user_docs_output'
  -z, --zipped          whether the files should be zipped or not
  -p, --per_file        whether to make separate userdocs for each file
```
