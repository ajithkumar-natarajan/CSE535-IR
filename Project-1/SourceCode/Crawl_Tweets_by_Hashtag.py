#!/usr/bin/env python
# coding: utf-8

import tweepy  
import time
import json
import datetime
!pip install emoji
import emoji
from tweepy.error import TweepError
 
target='Ajith' #Change as per the target hashtag
country="India" #Change as per POI's country

# access_token = '1166399406469517312-RxKaeptfEOrCT1kMjyj7bVpHZg1cLJ'
# access_token_secret = 'KShMyDDYfDMDmAHH2s23zFVGsbpRHryGmyzE2GQ12EFZ7'
# consumer_key = '0ikZzQrtivNo5gadzpEWTsO9l'
# consumer_secret = 'CtNdFgPWMyO6pSFbnOv2A8xnBZfn7H7K8dMdWYkEVrCWnfhmah'
consumer_key = "qiz1HJoLsPrVu72VhjulKuGCI"
consumer_secret = "ZjzL2b8T7HFZAOLEDbponHfSUlWKFScWH3x6WBkMs0ed1T4FOO"
access_token = "159181873-Y6biFJIWD2p7X0csBxgs4uHugZgz294ojm6erMnA"
access_token_secret = "ab2vzCNQYCK3Bfe3E6jHNjdzZxbAPdPccXRxvDSD8kQ14"
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)  
api = tweepy.API(auth,wait_on_rate_limit=True)

def round_to_hour(dt):
    dt_start_of_hour = dt.replace(minute=0, second=0, microsecond=0)
    dt_half_hour = dt.replace(minute=30, second=0, microsecond=0)

    if dt >= dt_half_hour:
        # round up
        dt = dt_start_of_hour + datetime.timedelta(hours=1)
    else:
        # round down
        dt = dt_start_of_hour

    return dt
def convertToObj(tweet,country):
    obj={}
    obj["poi_name"] = 'narendramodi' #Change to POI name
    obj["poi_id"] = "2670726740" #Change to POI ID
    obj["verified"] = "false"
    obj["country"] = country ## fill these based on the POI ,may be have a map with country as value and poi as key written manually
    obj["replied_to_tweet_id"] = tweet.in_reply_to_status_id_str
    obj["replied_to_user_id"] = tweet.in_reply_to_user_id_str
    if tweet.in_reply_to_user_id:
        obj["reply_text"] = tweet.full_text
    obj["tweet_text"] = tweet.full_text
    obj["tweet_lang"] = tweet.lang
    obj["hashtags"] = tweet.entities["hashtags"]
    obj["mentions"] = tweet.entities["user_mentions"]
    obj["tweet_urls"] = tweet.entities["urls"]
    obj["tweet_emoticons" ] = ''.join(c for c in tweet.full_text if c in emoji.UNICODE_EMOJI)
    obj["tweet_date"] = str(round_to_hour(tweet.created_at))
    obj["id"]  = tweet.id
    return obj
try:
    poi_tweet_file ='hashtag.json'
    for tweet in tweepy.Cursor(api.search, q='#'+target,tweet_mode='extended').items(2000):  #Change to required count. This will NOT be the number of hashtags corresponding to POI.
        if not hasattr(tweet, 'retweeted_status') and not tweet.in_reply_to_status_id:
            with open(target+'_hashtag.json', 'a+', encoding="utf8") as f:
                obj = convertToObj(tweet,country)
                json.dump(obj, f, ensure_ascii=False)
#         print(tweet._json)
except tweepy.TweepError:  
    time.sleep(60)