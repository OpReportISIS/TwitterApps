import sys
import re
import datetime
import argparse


#-----------------------------------------------------------------------
# SETTINGS - START
#-----------------------------------------------------------------------

# Default max. number of links to be scraped per target
# This setting will be ignored if user set the -n (max links) and/or -d (max days) in command line argument(s)
#
# https://dev.twitter.com/rest/reference/get/statuses/user_timeline
# Twitter API returns up to 3,200 of a user\'s most recent Tweets.
# That means it could return many thousands of links if no limit is set - long processing time

default_max_links = 1000


#-----------------------------------------------------------------------
# SETTINGS - END
#-----------------------------------------------------------------------


# Global variable
# Twitter API returns up to 3,200 of a user\'s most recent Tweets, which is - 16 pages x 200 tweets
max_pages = 16


# Import the Tweepy module
try:
    import tweepy

except ImportError:
    print "Please install Tweepy"
    sys.exit(1)


#-----------------------------------------------------------------------
# Loads Twitter API OAuth credentials from a configuration file
#-----------------------------------------------------------------------

def load_config():
    config = {}

    try:
        execfile("config.py", config)

    except:
        print "Please download and configure config.py"
        sys.exit(1)

    return config


#-----------------------------------------------------------------------
# Prints Elapse Time
#-----------------------------------------------------------------------

def elapse_time(sdatetime):
    # Show the elapsed time
    diff = datetime.datetime.now() - sdatetime
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print "\n-------------------------------------------------------------------------"
    print "Elapsed time: %02d:%02d:%02d\n" % (hours, minutes, seconds)


#-----------------------------------------------------------------------
# Scrapes links from target user's tweets
#-----------------------------------------------------------------------

def scrape_links(api, screen_name, user_id, is_all, is_excl_rts, max_links, max_days):
    global max_pages
    global default_max_links
    count = 0
    loop = True

    # If the exclude retweets flag is enabled
    if is_excl_rts:
        is_incl_rts = False
    else:
        is_incl_rts = True

    # Get the current time
    time_now = datetime.datetime.now()

    # If user didn't set both the max links and max days, use the default max links setting
    if (max_links == 0) and (max_days == 0):
        max_links = default_max_links

    # Iterates target user's tweets, 200 tweets per loop (page)
    for page in tweepy.Cursor(api.user_timeline, user_id=user_id, include_rts=is_incl_rts, count=200).pages(max_pages):

        # Iterates through each tweet
        for status in page:

            # If max days was set, and if the tweet was created earlier than the max days settings, skip that tweet
            if (max_days > 0) and ((time_now - status.created_at).days > max_days):
                continue

            # Otherwise, iterates through each links in that tweet
            else:
                for url in status.entities["urls"]:

                    # If scrapes all types of links (not just Twitter)
                    if is_all:
                        count += 1
                        with open("log_" + screen_name + "_" + str(user_id) + "_links.txt", "a") as log:
                            log.write("%s\n" % url['expanded_url'])

                    # If scrapes only Twitter links
                    else:
                        # Check if the link is a Twitter link
                        account = re.match(r"(?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:#!\/)?@?([^\/\?\s]*)",
                                           url['expanded_url'])

                        # If the URL is a Twitter link
                        if account:
                            count += 1
                            with open("log_" + screen_name + "_" + str(user_id) + "_links.txt", "a") as log:
                                log.write("%s\n" % url['expanded_url'])

                    # If max links was set and the number of extracted links reached that setting, exit the process
                    if (max_links > 0) and (count == max_links):
                        loop = False
                        break

            # Exit looping links in that tweet
            if loop is False:
                break

        # Exit looping tweets
        if loop is False:
            break

    # Prints execution summary
    print "\nLinks scraped from @%s (%s): %d" % (screen_name, str(user_id), count)


#-----------------------------------------------------------------------
# The main script that controls the flow
#-----------------------------------------------------------------------

def main():
    try:
        # Parse the optional command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--username", help="The Twitter username (screen name) to extract links")
        parser.add_argument("-f", "--file", help="Input file that contains Twitter usernames/IDs to extract links")
        parser.add_argument("-a", "--all", help="To scrape all links (not just Twitter links)", action="store_true")
        parser.add_argument("-e", "--exclude_rts", help="To exclude ReTweets", action="store_true")
        parser.add_argument("-d", "--days", help="The max. days of links to be extracted", type=int)
        parser.add_argument("-n", "--number", help="The max. count of links to be extracted", type=int)
        args = parser.parse_args()

        # If the username flag is enabled, get the target username from command line argument
        if args.username:
            screen_name = args.username
        else:
            screen_name = ""

        # If the file flag is enabled, read targets from the input file
        if args.file:
            input_file = args.file
        else:
            input_file = ""

        # If the all flag is enabled, scrape all links (not just Twitter links)
        if args.all:
            is_all = args.all
        # If the all flag is not enabled, scrape only Twitter links
        else:
            is_all = False

        # If the exclude ReTweet flag is enabled, skip links in ReTweets
        if args.exclude_rts:
            is_excl_rts = args.exclude_rts
        else:
            is_excl_rts = False

        # If the days flag is enabled, set the maximum days of links to be extracted
        if args.days:
            max_days = args.days
        else:
            max_days = 0

        # If the number flag is enabled, set the maximum number of links to be extracted
        if args.number:
            max_links = args.number
        else:
            max_links = 0

        # Load the configuration file
        config = load_config()

        # Initialize Tweepy Module
        auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
        auth.set_access_token(config["access_token"], config["access_token_secret"])
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        # Get the current time
        sdatetime = datetime.datetime.now()

        # If user didn't enter the screen name nor the input file, print message and exit
        if (not screen_name) and (not input_file):
            print "\nYou must enter -u or -f in the command:"
            print "\npython TwitterLinkExtractor -u <username> or,\npython TwitterLinkExtractor -f <filename>\n"
            exit(1)

        else:
            # Print progress status
            print "Scraping links..."

        # If user passed target screen name in command line argument
        if screen_name:
            print "Screen name  : %s" % screen_name

            # Get the user's Twitter ID
            user = api.get_user(screen_name)
            user_id = user.id
            print "->ID         : %s" % user_id

            # Scrape the links
            scrape_links(api, screen_name, user_id, is_all, is_excl_rts, max_links, max_days)

        # If the target username/ID links are in an input file
        elif input_file:
            try:
                f = open(input_file, 'r')
            except:
                print "Error: Can't open input file %s " % input_file
                sys.exit(1)

            for url in f:
                try:
                    url = url.strip()

                    if not url:
                        continue

                    print "\n-------------------------------------------------------------------------"
                    print "\nURL          : %s" % url

                    # Check if the URL is an ID link
                    account = re.match(r"(?:https?:\/\/)?(?:www\.)?twitter\.com\/intent/user\?user_id=(\d+)?", url)

                    # If the URL is an ID link
                    if account:
                        account = account.group(1)
                        user_id = account
                        print "ID           : %s" % str(account)

                        # Get the user's screen name
                        user = api.get_user(user_id)
                        screen_name = user.screen_name
                        print "->Screen name: %s" % screen_name

                        # Scrape the links
                        scrape_links(api, screen_name, user_id, is_all, is_excl_rts, max_links, max_days)

                    # Check if the URL is NOT an ID link
                    else:
                        # Check if the URL is a screen name link
                        account = re.match(r"(?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:#!\/)?@?([^\/\?\s]*)", url)

                        # If the URL is a screen name link
                        if account:
                            account = account.group(1)
                            screen_name = account
                            print "Screen name  : %s" % str(account)

                            # Get the user's ID
                            user = api.get_user(screen_name)
                            user_id = user.id
                            print "->ID         : %s" % user_id

                            # Scrape the links
                            scrape_links(api, screen_name, user_id, is_all, is_excl_rts, max_links, max_days)

                        # If the URL is NOT a screen name link (nor an ID link)
                        else:
                            raise ValueError()

                # Regular expression error
                except re.error as e:
                    if url:
                        print "\nRegex Error: %s" % str(e.reason)
                        with open("log_error.txt", "a") as log:
                            log.write("%s\n" % url)

                # Value error
                except ValueError:
                    if url:
                        print "\nError: Invalid URL %s " % url
                        with open("log_error.txt", "a") as log:
                            log.write("%s\n" % url)

        # Prints the elapse time
        elapse_time(sdatetime)

    # Tweepy error
    except tweepy.TweepError as e:
        print "\nTweepError: %s" % str(e.reason)

    # Keyboard interrupt
    except KeyboardInterrupt:
        print "\nQuit by keyboard interrupt sequence!"
        sys.exit()

    # Exception
    except Exception as e:
        print "\n%s" % str(e.message)

# Execute the main script
if __name__ == "__main__":
    main()
