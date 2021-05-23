#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
"""
Description:
    1. Scrape all comments from a given reddit thread
    2. Extract top level comments
    3. Save to a csv file

Author:
    Copyright (c) Ian Hussey 2016 (ian.hussey@ugent.be) 
    Released under the GPLv3+ license.

Known issues:
    None. 

Notes:
    1. Although the script only uses publiclly available information, 
    PRAW's call to the reddit API requires a reddit login (see line 47).
    2. Reddit API limits number of calls (1 per second IIRC). 
    For a large thread (e.g., 1000s of comments) script execution time may therefore be c.1 hour.
    3. Because of this bottleneck, the entire data object is written to a pickle before anything is discarded. 
    This speeds up testing etc.
    4. Does not extract comment creation date (or other properties), which might be useful. 
"""

# Dependencies
import praw
from praw.models import MoreComments
import os
import csv
import sys
import pickle
import Scraper_config as cfg

# Change directory to that of the current script
absolute_path = os.path.abspath(__file__)
directory_name = os.path.dirname(absolute_path)
os.chdir(directory_name)

# Acquire comments via reddit API
r = praw.Reddit(client_id=cfg.client_id, client_secret=cfg.client_secret, user_agent=cfg.bot_username)

# override this in config to decide which attributes to save from a comment object
def default_comment_to_list(comment):
    return [comment.body]

if hasattr(cfg, "comment_to_list"):
    comment_to_list = cfg.comment_to_list
else:
    comment_to_list = default_comment_to_list

def get_submission_comments(uniq_id):

    # Pull from reddit API or load from saved dump
    if (True):
        submission = r.submission(id=uniq_id)  # UNIQUE ID FOR THE THREAD GOES HERE - GET FROM THE URL
        #submission.comments.replace_more(limit=0, threshold=0)  # all comments, not just first page
        print("Saving pickle")
        # Save object to pickle
        output = open(cfg.output_file, 'wb')
        pickle.dump(submission, output, -1)
        output.close()
    else:
        print("Loading pickle")
        ## Load object from pickle
        pkl_file = open(cfg.output_file, 'rb')
        submission = pickle.load(pkl_file)
        #pprint.pprint(submission)
        pkl_file.close()

    # Extract first level comments only
    forest_comments = submission.comments  # get comments tree
    already_done = set()
    top_level_comments = []
    for comment in forest_comments:
        print("Username: %s" % comment.author)
        #if not hasattr(comment, 'body'):  # only comments with body text
        #    continue
        if comment.is_root:  # only first level comments
            if comment.id not in already_done:
                already_done.add(comment.id)  # add it to the list of checked comments
                if (isinstance(comment,MoreComments)):
                   print("This is a more comment")
                   continue
                try:
                    top_level_comments.append(str(comment.author))  # append to list for saving
                except AttributeError:
                    print("No author name")
    return top_level_comments

def get_subreddit_comments(uniq_id):
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    comStream = praw.helpers.comment_stream(r, uniq_id[3:], limit=limit) # Get the comment string
    comments = map(lambda _: [next(comStream).__str__()], range(limit)) # Get the raw string of each comment obj
    return list(comments) # Convert to list if running on Python3

uniq_id = cfg.uniq_id
if len(sys.argv) > 1:
    uniq_id = sys.argv[1]

if uniq_id[:3] == '/r/':
    top_level_comments = get_subreddit_comments(uniq_id)
else:
    top_level_comments = get_submission_comments(uniq_id)

print(top_level_comments)
# Save comments to disk
with open(cfg.output_csv_file, "w", encoding="utf-8") as output:
    output.write("Username,\n")
    for item in top_level_comments:
        output.write(str(item)+",\n")

# Upload to google sheets
if (cfg.gsheet_enable):
	import pygsheets
	import pandas as pd
    print("Uploading to Google Sheets")
	#authorization
	gc = pygsheets.authorize(service_file=cfg.service_file)

	# Create empty dataframe
	df = pd.DataFrame()

	# Create a column
	df['name'] = top_level_comments

	#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
	sh = gc.open('testing-brandon-algo')

	#select the first sheet 
	wks = sh[0]

	# clear
	wks.clear("*")
	#update the first sheet with df, starting at cell B2. 
	wks.set_dataframe(df,(1,1))

