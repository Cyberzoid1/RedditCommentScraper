# Reddit Comment Scraper
Forked from https://github.com/ianhussey/RedditCommentScraper. Modified to pull usernames from a thread

Scrape comments from a given thread on reddit.com using PRAW

## License
Copyright (c) Ian Hussey 2016 (ian.hussey@ugent.be)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

## Version
1.1 (5/22/2021)

## Install
Ubuntu & Debian based
**Install git**

`sudo apt install git`

**Clone this repo**

`git clone https://github.com/Cyberzoid1/RedditCommentScraper.git`

**Change directory**
`cd RedditCommentScrapper`

**Create a reddit app key**
Reddit apps: https://ssl.reddit.com/prefs/apps/
Tutorial: https://towardsdatascience.com/scraping-reddit-data-1c0af3040768

**Run setup script**
`./setup.sh`

Note api configs can be changed in `Scraper_config.py` file

### Google sheets
This feature allows for the csv to automatically be uploaded to a google sheet
1. Create a google sheet for a destination
2. Go to the google API Console https://console.developers.google.com/
3. Head over to the Google API Console.
4. Create a new project by selecting My Project -> + button
5. Search for 'Google Drive API', enable it.
6. Search for 'Google Sheets API', enable it.
7. Head over to 'Credentials' (sidebar), click 'Create Credentials' -> 'Service Account Key'
8. Open user and go to keys
9. Add Key > Create new key > JSON
10. Open up the JSON file, share your spreadsheet with the "XXX-compute@developer.gserviceaccount.com" email listed.
11. Save the JSON file wherever you're hosting your project, you'll need to load it in through Python later.

## Run Scrapper
`python3 Scraper.py <thread ID>`


## Description
1. Scrapes all comments from a given reddit thread
2. Extracts top level comments
3. Saves to a csv file

## Known issues
May not handle comments from deleted users

## Notes
1. Although the script only uses publiclly available information, PRAW's call to the reddit API requires a reddit login (see line 44).
2. Reddit API limits number of calls (1 per second IIRC). For a large thread (e.g., 1000s of comments) script execution time may therefore be c.1 hour.
3. To configure, `cp Scraper_config.py.example Scraper_config.py` and edit that file. To extract more comment fields such as author and creation date, override the `comment_to_list` function in the config file.

## References
https://erikrood.com/Posts/py_gsheets.html
https://pygsheets.readthedocs.io/en/latest/reference.html
