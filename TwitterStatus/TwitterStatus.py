import urllib2
import sys
import re
import time
import argparse

#-------------------------
# Settings - start
#-------------------------

# The number of seconds the script will wait if there is "Connection reset by peer" error
wait_seconds = 20


#-------------------------
# Settings - End
#-------------------------

# Global variables
iTotal = 0
iAlive = 0
iDuplicated = 0


#---------------------------
# To remove duplicated URLs
#---------------------------

def remove_duplicates(url, newlist):
    global iTotal
    global iAlive
    global iDuplicated

    if url not in newlist:
        iAlive += 1
        iTotal += 1
        newlist.append(url)
        print "[%s] Alive     : %s" % (str(iTotal), url)
        with open("log_alive.txt", "a") as log:
            log.write(url + "\n")
    else:
        iDuplicated += 1
        iTotal += 1
        print "[%s] Duplicated: %s" % (str(iTotal), url)
        with open("log_duplicated.txt", "a") as log:
            log.write(url + "\n")

    return True


#----------------------------------------
# The main script that controls the flow 
#----------------------------------------

def main():
    global iTotal       # Count of total handles
    global iAlive       # Count of alive handles
    global iDuplicated  # Count of duplicated handles
    iSuspended = 0      # Count of suspended handles
    iDeleted = 0        # Count of deleted handles
    iInvalid = 0        # Count of invalid handles
    newlist = []        # A list that keep track of duplicated URLs

    input_file = None
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--input_file', help='Enter the name of the input file')

    args = parser.parse_args()

    if args.input_file:
        input_file = args.input_file

    try:
        f = open(input_file, 'r')

    except:
        if not input_file:
            print "Execute: python TwitterStatus.py -f <filename.txt> (replace it with your input filename)"
        else:
            print "Error: Can't open input file %s " % input_file
        sys.exit(1)


    for url in iter(f):
        try:
            url = url.rstrip()

            if not url:
                continue

            response = urllib2.urlopen(url)
            returned_url = response.geturl()

            if "https://twitter.com/account/suspended" in returned_url:
                iSuspended += 1
                iTotal += 1

                print "[%s] Suspended : %s" % (str(iTotal), url)
                with open("log_suspended.txt", "a") as log:
                    log.write(url + "\n")
            else:
                url_r = re.match(r"(?:https:\/\/)?(?:http:\/\/)?(?:www\.)?twitter\.com/(#!/)?@?([^/\s]*)(/user\?user_id=\d+)?", returned_url.strip())

                if url_r is not None:
                    remove_duplicates(url, newlist)
                else:
                    iInvalid += 1
                    iTotal += 1
                    print "[%s] Invalid   : %s" % (str(iTotal), url)
                    with open("log_invalid_url.txt", "a") as log:
                        log.write(url + "\n")

        except urllib2.HTTPError, e:
            if str(e.code) == "404":
                iDeleted += 1
                iTotal += 1

                print "[%s] Deleted   : %s" % (str(iTotal), url)
                with open("log_deleted.txt", "a") as log:
                    log.write(url + "\n")
                    
        except urllib2.URLError, e:
            iInvalid += 1
            iTotal += 1

            if "104" in str(e.reason): 		# If failed for Connection reset by peer
                print "URL Error: %s" % str(e.reason)
                print "Sleep for %s seconds..." % (str(wait_seconds))
                time.sleep(wait_seconds)    # Sleeps for a predefined interval

            print "[%s] Invalid   : %s" % (str(iTotal), url)
            with open("log_invalid_url.txt", "a") as log:
                log.write(url + "\n")

        except ValueError:
            iInvalid += 1
            iTotal += 1

            print "[%s] Invalid   : %s" % (str(iTotal), url)
            with open("log_invalid_url.txt", "a") as log:
                log.write(url + "\n")

        except KeyboardInterrupt:
            print "\nQuit by keyboard interrupt sequence!"
            sys.exit(1)

        except:
            print "[%s] Error     : %s" % (str(iTotal), url)
            with open("log_error.txt", "a") as log:
                log.write(url + "\n")
                
    f.close()

    # Print the summary	
    print "\nProcessed  : " + str(iTotal)
    print "Alive      : " + str(iAlive)
    print "Suspended  : " + str(iSuspended)

    if iDeleted > 0:
        print "Deleted    : " + str(iDeleted)
    if iDuplicated > 0:
        print "Duplicated : " + str(iDuplicated)
    if iInvalid > 0:
        print "Invalid    : " + str(iInvalid)

# Execute the main script
main()
