from sys import stderr
print stderr, "Hello"
import os
import time
import re

from datetime import datetime, timedelta

#this package seems outdated, but it was super simple to set up
import tweepy

print stderr, "Very beginning..."

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

FOOTERS = ["#PULAKYELLING"]

ACCOUNTS = ["pulakm", "pennapps"]

#how often to check for new tweets (careful of twitter rate limiting)
DELAY = 12

#how long until we don't consider a tweet new?
#this is to deal with tweets bizarrely repeating
EXPIRED_TIME = timedelta(minutes=2)

URL_RE = ".+\..+"  # crude, but should handle most of what Pulak tweets

print stderr, "Doing auth"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

print stderr, "Auth done"


def send_tweet(message):
    final_message = message
    #add in footers (hashtags and users)
    for footer in FOOTERS:
        if len(final_message + " " + footer) <= 140:
            final_message += " " + footer
    try:
        print stderr, "Would have tweeted:"
        print stderr, final_message
        #api.update_status(final_message)
    except Exception as e:
        #this will print to heroku logs
        print stderr, e


def to_upper(message):
    upper_message = []
    for token in message.split(" "):
        if is_link(token):
            print stderr, "%s is a link" % token
            upper_message.append(token)
        else:
            upper_message.append(token.upper())
    return " ".join(upper_message)


def is_link(token):
    return True if re.match(URL_RE, token) else False

if __name__ == "__main__":
    print stderr, "Starting..."
    last_ids = {}  # keep track of id of last tweet from the stream
    for user in ACCOUNTS:
        last_ids[user] = 1
    while True:
        for user in ACCOUNTS:
            print stderr, "Getting tweets for", user
            try:
                #get most recent tweet
                tweet = api.user_timeline(user,
                                          since_id=last_ids[user], count=1)[0]
            except IndexError:
                #no tweeets found for this user
                print stderr, "Error getting tweet for", user
                continue
            last_ids[user] = tweet.id
            if(datetime.now() - tweet.created_at < EXPIRED_TIME):
                send_tweet(to_upper(tweet.text))  # Tweet! Tweet!

            time.sleep(DELAY)  # Avoid Twitter rate limiting
