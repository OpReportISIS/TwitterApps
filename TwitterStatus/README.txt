TwitterStatus (version 1.0)

=== 1. DESCRIPTION

A Python script that sorts Twitter target list into the following categories:
- Alive
- Suspended
- Deleted
- Invalid
- Duplicated

Accepted input formats (One URL per line):

    https://twitter.com/xxxxxxxxxx
    https://twitter.com/intent/user?user_id=xxxxxxxxxx
    
The output will be logged into respective log files for each category.

Note:

If the script failed for "[Errno 104] Connection reset by peer", it will wait for a predefined duration before resuming. The error is likely caused by Twitter refused the connection. This usually happened after making more than 1,000 requests.
    
If the default value doesn't correct the problem, please change it at step#3.


=== 2. REQUIREMENTS

Install Python 2.7.


=== 3. CONFIGURATION

If required, change this value to a longer wait duration, say 30 (seconds) or longer.

    wait_seconds = 20


=== 4. EXECUTION

Execute "python TwitterStatus.py -h" to show help

    Usage Example: python TwitterStatus.py -f filename.txt

    (replace filename.txt with the name of your input file)


=== 5. LICENSE

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
