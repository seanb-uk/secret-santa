# Secret Santa

Python script to replicate random matching of secret santa buyers to recipients.

Secret Santa is a popular tradition in offices and amongst other groups. The idea is that you buy a gift for another member of the group, assigned to you at random. The secret part is that you don't reveal who you're buying the gift for - and therefore, of course, you don't know who's buying a gift for you. The way it usually works is that you all put your names into a hat. Everyone takes a name without revealing it to the other members of the group - unless someone pulls their own name out, in which case you put all of the names back in the hat and try again.

The script generates a virtual draw. It works by taking a list of participants, randomly matching gift buyers with gift receivers and emailing the buyer. All valid combinations are possible, including reciprocal matches - i.e. where A buys for B and B buys for A.

The script can also email a full list of the buyer/recipient pairs to another email address. This can be useful if you know someone who isn't participating but is willing to act as a coordinator in case anyone loses their email and needs a reminder.

There is also a parameter to run the script multiple times without sending emails. This is just for fun - it's a single core performance test and proves the maths that it will be roughly *e* (2.718...) attempts to make a valid draw.

When you run it for a real draw make sure you set debug to False so you don't see the full list and spoil the secret!

For more on how it works and the maths behind it, see my blog post [here](https://seanb.co.uk/2020/11/secret-santa-for-the-covid-age/)

## Prerequisites

The script requires Python 3.x and was written and tested with Python 3.7.

In order to send emails, it must have access to an SMTP server that works with the standard smtplib library.


## Usage
```python secretsanta.py configfile```

Where configfile is a configuration file with the following parameters:

### Section: general
Parameter | Optional | Use
----------|----------|----
debug | Yes | True/False flag to control additional script output.
runs | Yes | Controls the number of times the script is run. Used for performance testing. Defaults to 1 if not provided. If runs is greater than one, emails will not be sent regardless of the send_email flag.

### Section: email
Parameter | Optional | Use
----------|----------|----
smtp_server | Yes | SMTP servername to use. Defaults to localhost if not provided.
smtp_port | Yes | SMTP port to use. Defaults to 25 if not provided.
smtp_username | Yes | SMTP username. Defaults to blank if not provided.
smtp_password | Yes | SMTP password. Defaults to blank if not provided.
smtp_from | Yes | SMTP from name. Defaults to blank if not provided.
send_email | Yes | True/False flag to control whether to send emails. Defaults to False if not provided.
summary_email | Yes | Email address of user to receive full list of buyers and recipients. Defaults to blank if not provided.

### Section: participants
Parameter | Optional | Use
----------|----------|----
name | No | Repeated for each participant, where name is the participants name and the value is their email address.



## Examples

Take the following config file named secretsanta.conf:

```
[general]
debug = True

[email]
send_email = False


[participants]
A = a@example.org
B = b@example.org
C = c@example.org
D = d@example.org
E = e@example.org
```
Run the script:
```
> python secretsanta.py secretsanta.conf
Debug output on
Sending emails: False
Number of runs: 1
A is buying for B
B is buying for C
C is buying for D
D is buying for E
E is buying for A
All done! It took 2 draws to get a result
```

Setting runs to 10,000,000 the output is:

```
Debug output on
Sending emails: False
Number of runs: 10000000
Total number of runs    : 10000000
Average number of draws : 2.7266681
Maximum number of draws : 37
Time taken              : 130.24s
```

## Example emails

The email to the buyers will be:
```
Subject: Secret Santa
Hi <buyername>,

Your Secret Santa recipient is <recipientname>

Please don't reply to this message, otherwise I'll know who you got!

Thanks,

<from>
```

The summary email will be:
```
Subject: Secret Santa - Full list
In case anyone forgets, the full list of Secret Santas is as follows:

<buyername> is buying for <recipientname>
<buyername> is buying for <recipientname>
<buyername> is buying for <recipientname>
```
