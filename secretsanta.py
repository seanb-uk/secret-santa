# Secret Santa
#
# Usage: python secretsanta.py <configfile>
#
# Takes a list of participants in secret santa and assigns recipients to buyers.
# Options:
#  send an email summary to an additional address.
#  run multiple times for stats and performance testing.

import sys
import smtplib
import random
import configparser
import time

from email.message import EmailMessage

def send_mail(recipient, message, subject):

    if debug: print("Sending email to {} with subject {}".format(recipient, subject))
    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = "{} <{}>".format(email_from, smtp_username)
    msg['To'] = recipient
    msg.set_content(message)

    try:
        s = smtplib.SMTP(smtp_server, smtp_port)
        if smtp_username and smtp_password:
            s.login(smtp_username, smtp_password)
        s.send_message(msg)
    except:
        # No apologies here for a generic catch-all, as there are so many different
        # exceptions that can occur with email and this is a quick and dirty script.
        print("Error sending email: {}".format(sys.exc_info()[0]))
        sys.exit(1)        

start_time = time.perf_counter()
config = configparser.ConfigParser()
config.optionxform = lambda option: option  # Preserve case

# Get all of the config file options
try:
    config_file = sys.argv[1]
    with open(config_file) as f:
        config.read(config_file)
    recipients = list(config['participants'].keys())
    buyers = list(config['participants'].keys())

    # SMTP Configuration settings
    smtp_server = config.get('email', 'smtp_server', fallback='localhost')
    smtp_port = config.get('email', 'smtp_port', fallback=25)
    smtp_username = config.get('email', 'smtp_username', fallback = '')
    smtp_password = config.get('email', 'smtp_password', fallback = '')
    email_from = config.get('email', 'from', fallback = '')

    # Send email - determines whether to send the results
    # Defaults to false for testing
    send_email = config.getboolean('email', 'send_email', fallback=False) 

    # Optional email address for a summary email of all buyers/recipients
    summary_email = config.get('email', 'summary_email', fallback='')     

    debug = config.getboolean('general', 'debug', fallback=False)           # Self explanatory - 

    # Number of times to run the algorithm.
    # Useful for stats and performance testing.
    # If this is set greater than 1, emails will not be sent
    runs = config.getint('general', 'runs', fallback = 1)

except IndexError:
    print("Please specify a config file")
    sys.exit(1)
except IOError:
    print("Config file {} not readable".format(config_file))
    sys.exit(1)
except KeyError as e:
    print("Config file is missing key: {}".format(e))
    sys.exit(1)


if debug: 
    print("Debug output on")
    print("Sending emails: {}".format(send_email))
    print("Number of runs: {}".format(runs))

# Make sure that emails aren't sent when doing multiple runs
if runs > 1:
    send_email = False

max_draws = 0
total_draws = 0

# Shuffle recipients and match to buyers. 
# This method allows for mutual pairs (a buys for b and b buys for a).
# It takes on average 2.72 attempts to get a valid set - actually 'e' attempts to be precise :)

for run in range(runs):

    valid = False
    draws = 0
    while not valid:

        results = {}
        random.shuffle(recipients)

        valid = True
        draws = draws + 1

        for i in range(len(buyers)):
            if buyers[i] == recipients[i]:
                valid = False
                break
            results[buyers[i]] = recipients[i]
    
    if draws > max_draws:
        max_draws = draws
    
    total_draws = total_draws + draws


if runs == 1:
    summary = []

    for buyer in results:
        summary.append("{} is buying for {}".format(buyer, results[buyer]))

        if send_email:
            message = """
Hi {},

Your Secret Santa recipient is {}

Please don't reply to this message, otherwise I'll know who you got!

Thanks,

{}
    """.format(buyer, results[buyer], email_from)
            send_mail(config['participants'][buyer], message, "Secret Santa")


    if send_email and summary_email:
        if debug: print("Sending summary email to {}".format(summary_email))
        message = """
In case anyone forgets, the full list of Secret Santas is as follows:

{}
    """.format("\n".join(summary))
        send_mail(summary_email, message, "Secret Santa - Full list")

    if debug: 
        print("\n".join(summary))
    
    print("All done! It took {} draws to get a result".format(draws))

else:
    print("Total number of runs    : {}".format(runs))
    print("Average number of draws : {}".format(total_draws / runs))
    print("Maximum number of draws : {}".format(max_draws))
    print("Time taken              : {:.2f}s".format(time.perf_counter() - start_time))


