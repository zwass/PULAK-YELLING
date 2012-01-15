import sys
import os
import time

#this package seems outdated, but it was super simple to set up
import tweepy

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

FOOTERS = ["#PULAKYELLING"]

ACCOUNTS = ["pulakm", "pennapps"]

DELAY = 12

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def send_tweet(message):
    final_message = message
    #add in footers (hashtags and users)
    for footer in FOOTERS:
        if len(final_message + " " + footer) <= 140:
            final_message += " " + footer
    final_message = final_message.upper()
    try:
        api.update_status(final_message)
    except Exception as e:
        #this will print to heroku logs
        print e

if __name__ == "__main__":
    last_ids = {} #keep track of id of last tweet from the stream
    for user in ACCOUNTS:
        last_ids[user] = 1
    while True:
        time.sleep(DELAY) #Avoid Twitter rate limiting
        for user in ACCOUNTS:
            try:
                #get most recent tweet
                tweet = api.user_timeline(user, since_id=last_ids[user], count=1)[0]
            except IndexError:
                #no tweeets found for this user
                continue
            last_ids[user] = tweet.id
            send_tweet(tweet.text) #Tweet! Tweet!
