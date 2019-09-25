import json
import tweepy
import time
from config import *

#TODO: implement a way to get rid of the pictures; Get complete text working on Python, no more '...'
#TODO: like anyone that responds to our tweets

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        #prints out both name and message of tweet
        print(f"{tweet.user.name}:{tweet.text}")
        print()

        #temporarily stores raw tweet text
        tweettext = tweet.text

        #stores tweet id, used to reply to comments
        tid = tweet.id
        #stores "@" name, also needed to reply to comments
        sn = tweet.user.screen_name

        #boolean value that checks if everything is in order
        good_to_go = False

        #checks all forms of "im" and splits the text acccordingly.
        #TODO: change these to switch statements if those exist in Python
        if " im " in tweettext:
            newtweettext = tweettext.partition(" im ")[2]
            good_to_go = True

        elif " Im " in tweettext:
            newtweettext = tweettext.partition(" Im ")[2]
            good_to_go = True

        elif " IM " in tweettext:
            newtweettext = tweettext.partition(" IM ")[2]
            good_to_go = True

        elif " iM " in tweettext:
            newtweettext = tweettext.partition(" iM ")[2]
            good_to_go = True

        elif "im " in tweettext:
            newtweettext = tweettext.partition("im ")[2]
            good_to_go = True

        elif "Im " in tweettext:
            newtweettext = tweettext.partition("Im ")[2]
            good_to_go = True

        elif "IM " in tweettext:
            newtweettext = tweettext.partition("IM ")[2]
            good_to_go = True

        elif "iM " in tweettext:
            newtweettext = tweettext.partition("iM ")[2]
            good_to_go = True

        else:
            newtweettext = "ERROR: NO 'IM' FOUND"
            good_to_go = False

        #if tweet.retweeted_status does not exist, it throws an exception, so this exists to handle that, and to see if current tweet is a retweet or not
        if good_to_go:
            try:
                rt = tweet.retweeted_status
                good_to_go = False

            except AttributeError:
                print("NOT A RETWEET")
                good_to_go = True
                pass


        #if good_to_go is good, everything goes forward
        if good_to_go:
            #both deals with invalid urls, and duplicate message while both printing and exporting dad joke
            try:
                api.update_status("@" + sn + " Hey \"" + newtweettext + "\", I'm Dad", tid)
                print("@" + sn + " Hey \"" + newtweettext + "\", I'm Dad", tid)
                print("---------------------------------------------------------------------------------")

            except tweepy.TweepError as error:
                if error.api_code == 187:
                    print("duplicate message")
                else:
                    try:
                        api.update_status("@" + sn + " Hey \"" + newtweettext + "\", I'm Dad", tid)
                        print("@" + sn + " Hey \"" + newtweettext + "\", I'm Dad", tid)
                        print("---------------------------------------------------------------------------------")

                    except tweepy.TweepError as error:
                        if error.api_code == 408:
                            print("invalid url")
                        else:
                            raise error

        # waits 10 minutes after a tweet
        time.sleep(120)

    def on_error(self, status):
        print("Error detected")


# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN,TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener, tweet_mode='extended')
stream.filter(track=[" im "], languages=["en"])
