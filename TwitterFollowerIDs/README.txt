TwitterFollowersID (version 1.0)

The script is for known #OpISIS hunters only. Kindly contact me on my Twitter account if you need the script. Thank you for your understanding.


=== 1. DESCRIPTION

A Python script that scrapes the IDs of a Twitter handle's followers and followings. It can also scrapes from a target list file.

Accepted input formats:

i.  Command line input: Twitter username (screen name) or ID
ii. Target list file 
      

Output format:
https://twitter.com/intent/user?user_id=xxxxxxxxxx

The output files are named by the target handle's username and ID
e.g.

log_OpReportISIS_4840928547_followers.txt
log_OpReportISIS_4840928547_friends.txt


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

Execute "python TwitterFollowerIDs.py -h" to show help

Usage examples:

i.  To scrape followers of a Twitter handle

    1.  By username (screen name)
        python TwitterFollowerIDs.py -u username (replace username accordingly)
        
    2.  By user ID
        python TwitterFollowerIDs.py -i userID (replace userID accordingly)
        
ii. To scrape both followers and followings of a Twitter handle by username

    python TwitterFollowerIDs.py -u username -a (replace username accordingly)

iii.To scrape followers and followings from a target list file
  
    The target list file may contain username and/or ID formats (one URL per line):
    
    https://twitter.com/xxxxxxxxxx
    https://twitter.com/intent/user?user_id=xxxxxxxxxx
    
    python TwitterFollowerIDs.py -f filename.txt -a 

    (replace filename.txt with your input file's name)
  
  
=== 5. LICENSE

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
