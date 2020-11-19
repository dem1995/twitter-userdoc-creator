"""
Takes in a .jsonl file of tweets and spits out a series of .jsonol files of tweets, one file per Twitter user.
"""

import json
import argparse
import os
from collections import defaultdict

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('input', nargs="+", help="The .jsonl tweet files to take in to produce user documents from")
parser.add_argument('-o', '--outdir', nargs="?", default='user_docs_output', 
                    help="The directory to output the tweet files to. Defaults to 'user_docs_output'")
args = parser.parse_args()

# Create the output directory, if needed
if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)

# Generator that goes through each line of the input files
def lines_of_files():
    for input_file in args.input:
        with open(input_file, encoding="utf8") as input_file_lines:
            for line in input_file_lines:
                yield line


# Get a list of tweet json strings for each user
user_tweets_lookup = defaultdict(list)
for line in lines_of_files():
    tweet = json.loads(line)
    user_id = tweet['user']['id']
    if 'extended_tweet' in tweet:
        text = tweet['extended_tweet']['full_text']

    text = tweet['full_text'].replace('\n', ' ')
    user_tweets_lookup[user_id].append(text)

# For each user id, create a user document
for user_id, user_tweets in user_tweets_lookup.items():
    with open(f"{args.outdir}/{user_id}.userdoc", encoding="utf8", mode='w+') as user_doc:
        user_doc.write('\n'.join(user_tweets))