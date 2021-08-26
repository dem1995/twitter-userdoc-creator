"""
Takes in a .jsonl file of tweets and spits out a series of .jsonol files of tweets, one file per Twitter user.
"""

import json
import argparse
import os
import zipfile
from collections import defaultdict

def tweet_files_to_userdocs(tweet_files):
	# Generator that goes through each line of the input files
	def lines_of_files():
		for input_file in tweet_files:
			with open(input_file, encoding="utf8") as input_file_lines:
				for line in input_file_lines:
					yield line

	# Get a list of tweet json strings for each user
	user_tweets_lookup = defaultdict(list)
	for line in lines_of_files():
		tweet = json.loads(line)
		user_id = tweet['author_id']
		if 'extended_tweet' in tweet:
			text = tweet['extended_tweet']['full_text']

		text = tweet['text'].replace('\n', ' ')
		text = f"{tweet['id']}\t{tweet['created_at']}\t{text}"
		user_tweets_lookup[user_id].append(text)

	return user_tweets_lookup

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('input', nargs="+", help="The .jsonl tweet files to take in to produce user documents from")
	parser.add_argument('-o', '--outdir', nargs="?", default='user_docs_output',
	                    help="The directory to output the tweet files to. Defaults to 'user_docs_output'")
	parser.add_argument('-z', '--zipped', action='store_true', help='whether the files should be zipped or not')
	parser.add_argument('-p', '--per_file', action='store_true', help='whether to make separate userdocs for each file')
	args = parser.parse_args()

	# If we are getting userdocs for each file, we isolate each file into its own collection for processing
	if args.per_file:
		userdoc_source_collections = [[tweetfile] for tweetfile in args.input]
	else:
		userdoc_source_collections = [args.input]

	for userdoc_source_collection in userdoc_source_collections:
		if args.per_file:
			suboutdir = "/" + userdoc_source_collection[0].rpartition('/')[2].rpartition('.')[0]
		else:
			suboutdir = ""

		# Create the output directory, if needed
		if not args.zipped and not os.path.exists(f"{args.outdir}{suboutdir}"):
			os.makedirs(f"{args.outdir}{suboutdir}")

		# Retrieve a mapping from user ids to user tweets
		user_tweets_lookup = tweet_files_to_userdocs(userdoc_source_collection)

		if not args.zipped:
			# For each user id, make a file for the user document
			for user_id, user_tweets in user_tweets_lookup.items():
				with open(f"{args.outdir}{suboutdir}/{user_id}.userdoc", encoding="utf8", mode='w+') as user_doc:
					user_doc.write('\n'.join(user_tweets))
		else:
			# For each user id, make a file for the user document in a compressed file
			filepath = f"{args.outdir}.zip"
			with zipfile.ZipFile(filepath, mode='a') as zf:
				for user_id, user_tweets in user_tweets_lookup.items():
					zf.writestr(f"{args.outdir}{suboutdir}/{user_id}.userdoc", '\n'.join(user_tweets))
