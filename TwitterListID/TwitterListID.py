import sys
import datetime
import argparse


try:
    import tweepy

except ImportError:
    print "Please install Tweepy"
    sys.exit(1)


#-----------------------------------------------------------------------
# Loads Twitter API oauth credentials from a configuration file
#-----------------------------------------------------------------------

def load_config():
    config = {}

    try:
        execfile("config.py", config)

    except (OSError, IOError) as e:
        print "Error: %s " % str(e)
        sys.exit(1)

    return config


#-----------------------------------------------------------------------
# Print Elapse Time
#-----------------------------------------------------------------------

def elapse_time(sdatetime):
    # Show the elapsed time
    diff = datetime.datetime.now() - sdatetime
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print "\n-------------------------------------------------------------------------"
    print "Elapsed time: %02d:%02d:%02d\n" % (hours, minutes, seconds)


#-----------------------------------------------------------------------
# The main script that controls the flow
#-----------------------------------------------------------------------

def main():
    try:
        count = 0

        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--username', help='The list owner\'s name')
        parser.add_argument('-s', '--slug', help='The name of the list')

        # Parse the optional command line arguments
        args = parser.parse_args()

        if args.username:
            owner = args.username
        else:
            owner = ""

        if args.slug:
            slug = args.slug
        else:
            slug = ""

        # Load the configuration file
        config = load_config()

        # Initialize Tweepy Module
        auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
        auth.set_access_token(config["access_token"], config["access_token_secret"])
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        # Get the current time
        sdatetime = datetime.datetime.now()

        # Print progress status
        print "Scraping list %s..." % slug

        # Iterate the Tweepy cursor through pages
        for page in tweepy.Cursor(api.list_members, owner_screen_name=owner, slug=slug).pages():
            for user in page:
                count += 1
                with open("log_" + owner + "_" + slug + ".txt", "a") as log:
                    log.write("https://twitter.com/intent/user?user_id=%d\n" % user.id)

        # Print progress status
        print "IDs scraped from list %s: %d" % (slug, count)

        # Print the elapse time
        elapse_time(sdatetime)

    # Tweepy error
    except tweepy.TweepError as e:
        print "\nTweepError: %s" % str(e.reason)

    # Keyboard interrupt
    except KeyboardInterrupt:
        print "\nQuit by keyboard interrupt sequence!"

    except Exception as e:
        print "\n%s" % str(e.message)
        exit(1)

# Execute the main script
main()
