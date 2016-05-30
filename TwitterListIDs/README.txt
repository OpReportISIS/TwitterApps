TwitterListIDs (version 1.0)


=== 1. DESCRIPTION

A Python script that scrapes members' IDs from a Twitter list.

The format of a Twitter list is:
https://twitter.com/<owner screen name>/lists/<list slug>

Output format:
https://twitter.com/intent/user?user_id=xxxxxxxxxx

The output files are named by the list owner's screen name and list's slug
e.g.
log_OpReportISIS_list1.txt


=== 2. REQUIREMENTS

i.  Install Python 2.7.

ii. Install Tweepy (Twitter API library for Python) in your system.

    Download and installation intructions:

    https://github.com/tweepy/tweepy
    
    
=== 3. CONFIGURATION

https://twittercommunity.com/t/how-to-get-my-api-key/7033

i.  Create a new Twitter Application at https://apps.twitter.com/

ii. Click the "Keys and Access Tokens" tab.

    Under the "Your Access Token" section, click "Create my access token" 

    Copy the settings into your config.py

    CONSUMER_KEY
    CONSUMER_SECRET
    ACCESS_TOKEN
    ACCESS_TOKEN_SECRET
    
iii. Save "config.py"


=== 4. EXECUTION

Execute "python TwitterListIDs.py -h" to show help

Usage examples:

python TwitterListIDs.py -u username -s listslug

(replace username and listslug accordingly)


=== 5. LICENSE

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
