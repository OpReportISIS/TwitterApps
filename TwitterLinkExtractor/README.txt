TwitterLinkExtractor (version 1.0)

=== 1. DESCRIPTION

A Python script that scrapes links from the tweets of Twitter account(s).

Accepted input formats:

Command line: username

or,
input file (one URL per line):

https://twitter.com/xxxxxxxxx
https://twitter.com/intent/user?user_id=xxxxxxxxx


=== 2. REQUIREMENTS

i.  Install Python 2.7.

ii. Install Tweepy (Twitter API library for Python) in your system.

Download and installation intructions:

https://github.com/tweepy/tweepy


=== 3. CONFIGURATION

i.  Set the the default maximum number of links to be scraped per target in TwitterLinkExtractor.py: 

e.g. default_max_links = 1000

NOTE:
This setting will be ignored if user set either the -n (max links) or the -d (max days) command line argument.

https://dev.twitter.com/rest/reference/get/statuses/user_timeline

Twitter API returns up to 3,200 of a user's most recent Tweets. That means it could return many thousands of links if no limit is set.


ii.  Twitter OAuth Credentials

https://twittercommunity.com/t/how-to-get-my-api-key/7033

Create a new Twitter Application at https://apps.twitter.com/

Click the "Keys and Access Tokens" tab.

Under the "Your Access Token" section, click "Create my access token".

Copy the settings into your config.py:

CONSUMER_KEY
CONSUMER_SECRET
ACCESS_TOKEN
ACCESS_TOKEN_SECRET

iii. Save config.py.


=== 4. EXECUTION

Execute "python TwitterLinkExtractor.py -h" to show help.

usage: TwitterLinkExtractor.py [-h] [-u USERNAME] [-f FILE] [-a] [-e]
                               [-d DAYS] [-n NUMBER]

  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        The Twitter username (screen name) to extract links
  -f FILE, --file FILE  Input file that contains Twitter usernames/IDs to
                        extract links
  -a, --all             To scrape all links (not just Twitter links)
  -e, --exclude_rts     To exclude ReTweets
  -d DAYS, --days DAYS  The max. days of links to be extracted
  -n NUMBER, --number NUMBER
                        The max. count of links to be extracted

Usage Examples: 
i. From a target user

   - To extract only Twitter links:
     python TwitterLinkExtractor.py -u <username>

   - To extract all types of links (not limited to Twitter):
     python TwitterLinkExtractor.py -u <username> -a

   - By default, it extracts links from all retweets.

     To exclude links from retweets:
     python TwitterLinkExtractor.py -u <username> -e

   - To extract links from tweets NOT older than a day:
     python TwitterLinkExtractor.py -u <username> -d 1

   - To extract maximum 350 links:
     python TwitterLinkExtractor.py -u <username> -n 350

   - To extract links from tweets NOT older than 2 days
     and maximum 500 tweets:
     python TwitterLinkExtractor.py -u <username> -d 2 -n 500

   NOTE: 
   If both "-d" and "-n" are not set, the script will return no more
   than the maximum number of links set in 3.i: default_max_links
	
ii. From an input file
    Other parameters stated in 4.i. are also supported (except -u)
    
    python TwitterLinkExtractor.py -f <filename.txt>

    
(replace username and filename.txt accordingly)


=== 5. LICENSE

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
