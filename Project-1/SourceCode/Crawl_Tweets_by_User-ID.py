import datetime
import tweepy
import json
import time
!pip install emoji
import emoji
import os


consumer_key="wiIMQT1sYEkCblbw6ADRc94wv"
consumer_secret="i2GabnzSO3jaTB777mO7PdiAJhREnxViroDeOIxu6IBF5AHNNG"
access_token="1459736401-CIKdFpgWZ2JGlXLUkVBfKULzNqiBmlzxIGLmdI1"
access_token_secret="EYmqH8ycJnf8rH4sdnkvTAXxNub3GxEUpLQJUlCBKMjAe"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
original_tweet=0
filtered_count=0
reply_count=0
list=[]
min_date = datetime.datetime(2019, 9, 4)
max_date = datetime.datetime(2019, 9 , 11)
poi = 'joshscampbell'
poi_tweet_file = poi + '-OnlyTweets-tweets.json'
poi_replies_file = poi + '-OnlyTweets-replies.json'
def convertToObj(tweet):
    obj={}
    obj["poi_name"] = tweet.user.screen_name
    obj["poi_id"] = tweet.user.id
    obj["verified"] = tweet.user.verified
    obj["country"] = "USA"
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
    return obj

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

for tweet in tweepy.Cursor(api.user_timeline, screen_name=poi, tweet_mode='extended', include_rts=False, exclude_replies=True).items(2000):
 if not hasattr(tweet, 'retweeted_status') and not tweet.in_reply_to_status_id:
    original_tweet+=1
    print(original_tweet)
    with open(poi_tweet_file, 'a+', encoding="utf8") as f:
     obj=convertToObj(tweet)
     json.dump(obj, f, ensure_ascii=False)
    if tweet.created_at < max_date and tweet.created_at > min_date :
      filtered_count+=1
      list.append(tweet.id)
 time.sleep(1)
RC=0
replies=[]
# for tweet_id in list:
#     reply_count = 0
#     for tweet in tweepy.Cursor(api.search, q='to:'+poi, since_id=tweet_id, max_id=None,count=100,tweet_mode='extended').items(2000):
#       if tweet.in_reply_to_status_id == tweet_id:
#         if reply_count <= 20 :
#          RC+=1
#          reply_count+=1
#          replies.append(tweet)
#          with open(poi_replies_file, 'a+') as f:
#           json.dump(tweet._json, f)
# #          print(tweet.full_text)
#         else:
#          break
# time.sleep(1)


os.rename(poi + '-OnlyTweets-tweets.json', poi+'-tweets-'+str(original_tweet)+'.json')
print('Original count', original_tweet)
print('Filtered Replies count', filtered_count)
print('Tot Replies count', RC, len(replies), list)