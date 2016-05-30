TwitterIDConverter (version 1.1)

=== 1. DESCRIPTION

A Python script that mass converts Twitter username links to ID links.

Accepted input formats (One URL per line):

	http://twitter.com/xxxxxxxxx
	https://twitter.com/xxxxxxxxx
	http://www.twitter.com/xxxxxxxxx
	https://www.twitter.com/xxxxxxxxx

Output format:

	https://twitter.com/intent/user?user_id=xxxxxxxxxx

=== 2. REQUIREMENTS

i. Install Python 2.7.

ii. Install Tweepy (Twitter API library for Python) in your system.

	Download and installation intructions:
	https://github.com/tweepy/tweepy

=== 3. CONFIGURATION

https://twittercommunity.com/t/how-to-get-my-api-key/7033

i.  Create a new Twitter Application at https://apps.twitter.com/

ii. Click the "Keys and Access Tokens" tab.

    Under the "Your Access Token" section, click "Create my access token" 	

    Copy the settings into your TwitterIDConverter.py

	CONSUMER_KEY
	CONSUMER_SECRET
	ACCESS_TOKEN
	ACCESS_TOKEN_SECRET

iii. Save "TwitterIDConverter.py"

=== 4. EXECUTION

Execute "python TwitterIDConverter.py -h" to show help

	Usage Example: python TwitterIDConverter.py -f filename.txt

	(replace filename.txt with the name of your input file)

=== 5. LICENSE

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
