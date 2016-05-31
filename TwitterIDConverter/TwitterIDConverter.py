import sys
import re
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
# The main script that controls the flow
#-----------------------------------------------------------------------

def main():
    count = 0
    input_file = None

    # Parse the optional command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--input_file', help='Enter the filename that contains the Twitter usernames')
    args = parser.parse_args()

    # If the optional argument -f was set
    if args.input_file:
        input_file = args.input_file

    # Load the configuration file
    config = load_config()

    # Initialize Tweepy Module
    auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
    auth.set_access_token(config["access_token"], config["access_token_secret"])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Try to open the input file
    try:
        f = open(input_file, 'r')

    except:
        if not input_file:
            print "Execute: python TwitterIDConverter.py -f <filename.txt> (replace it with your input f$
        else:
            print "Error: Can't open input file %s " % input_file
        sys.exit(1)

    for url in f:
        try:           
            url = url.strip()
            if not url:
                continue

            count += 1
            account = re.match(r"(?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:#!\/)?@?([^\/\?\s]*)", url)
            if not account:
                raise ValueError(url)

            account = account.group(1)
            user = api.get_user(account)

            print "[{:0d}] {:35s} --> {:0d}".format(count, url, user.id)

            with open("log_IDs.txt", "a") as log:
               log.write("https://twitter.com/intent/user?user_id=%s\n" % (user.id))

        except re.error:
            if url:
                print "[{:0d}] {:35s} --> Error: Invalid URL".format(count, url)
                with open("log_IDs_error.txt", "a") as log:
                    log.write("%s\n" % url)

        except tweepy.TweepError:
            if url:
                print "[{:0d}] {:35s} --> Error: Suspended or deleted".format(count, url)
                with open("log_IDs_error.txt", "a") as log:
                    log.write("%s\n" % url)

        except ValueError:
            if url:
                print "[{:0d}] {:35s} --> Error: Invalid URL".format(count, url)
                with open("log_IDs_error.txt", "a") as log:
                    log.write("%s\n" % url)

        except KeyboardInterrupt:
            print "\nQuit by keyboard interrupt sequence!"
            sys.exit()

        except:
            if url:
                print "[{:0d}] {:35s} --> Error".format(count, url)
                with open("log_IDs_error.txt", "a") as log:
                    log.write("%s\n" % url)


# Execute the main script
main()
