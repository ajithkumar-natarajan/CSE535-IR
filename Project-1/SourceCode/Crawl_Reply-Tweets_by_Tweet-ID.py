import datetime
import tweepy
import json
import time
!pip install emoji
import emoji
from tweepy.error import TweepError
import os

consumer_key ="JXhZID3p14VwHORjNl69lgiYL"
consumer_secret = "7ZQbHX78g6hHLAt4CAFuFYpx1WugaNZzIyfTKP4i3jr8iiKZKq"
access_token = "1459736401-hfUCedD01e6z4BlDYLA6vIFzVKYpyPJDUfPgpiO"
access_token_secret = "ovTnQeshZn0NrtViqETSKisxteMnI077FU2ESx59X0JiR"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
print(api)
original_tweet=0
filtered_count=0
reply_count=0
RC=0



def extract_tweets(poi,max_id,id_lis):
    try:
        original_tweet=0
        filtered_count=0
        poi_tweet_file = poi + '--tweets.json'
        end_encountered = 0
        while(end_encountered == 0):

            #print(max_id)
            if max_id == 0:
                print("Default call")
                cur = tweepy.Cursor(api.user_timeline, screen_name=poi, tweet_mode='extended').items(2000)
            else:
                print("Max Id call")
                cur = tweepy.Cursor(api.user_timeline, screen_name=poi,max_id = str(max_id), tweet_mode='extended').items(2000)
            for tweet in cur:
                 max_id = tweet.id
                 #print(hasattr(tweet, 'retweeted_status'))
                 if not hasattr(tweet, 'retweeted_status') and not tweet.in_reply_to_status_id:
                    original_tweet+=1
                    if tweet.created_at < min_date:
                        print(tweet.created_at)
                        end_encountered = 1
                        break
                    if tweet.created_at > max_date:
                        continue
                    print(tweet.id)
        #             print("before Date check is "+str(tweet.created_at))
        #             print(tweet.created_at < max_date)
        #             print(tweet.created_at > min_date)
                    filtered_count+=1
                    id_lis.append(tweet.id)
        #             print("after Date check is "+str(tweet.created_at))


                    with open(poi_tweet_file, 'a+', encoding="utf8") as f:
                        obj = convertToObj(tweet)
                        print(obj["tweet_date"])

                        json.dump(obj, f, ensure_ascii = False)
    except TweepError as e:
        time.sleep(10)
        print(e)
        extract_tweets(poi,max_id,id_lis)



def extract_replies(poi,id_list,replies_lis,replies_count_map,max_id):
    try:
        poi_replies_file = poi + '-replies.json'
        i =0;
        since_id = min(id_list)
        # max_id = None
        # temp_id = None
        total_tweets = 0
        last_max_id = max_id
        extraction_finished = 0;
        while (1):
            print("Fetching tweets for since id :"+str(since_id)+" max id is :"+str(max_id))
            if max_id == 0:
                cur = tweepy.Cursor(api.search, q='to:'+poi, since_id=since_id, count=1000,tweet_mode='extended').items(1000)
            else:
                cur = tweepy.Cursor(api.search, q='to:'+poi, since_id=since_id, max_id=max_id,count=1000,tweet_mode='extended').items(1000)
            for tweet in cur:
                max_id = tweet.id
                if tweet.in_reply_to_status_id in id_list:
                    total_tweets = total_tweets+1
                    if replies_count_map[tweet.in_reply_to_status_id] <= 20:
                        #print("Found reply for tweet :"+str(tweet.in_reply_to_status_id) +" ,reply with id : "+tweet.id+)
                        replies_lis.append(tweet)
                        replies_count_map[tweet.in_reply_to_status_id] = replies_count_map[tweet.in_reply_to_status_id] + 1
                        print("Found reply for tweet :"+str(tweet.in_reply_to_status_id) +" ,reply with id : "+str(tweet.id)+" ,count is" + str(replies_count_map[tweet.in_reply_to_status_id]))
                        with open(poi_replies_file, 'a+' , encoding="utf8") as f:
                            obj = convertToObj(tweet)
                            obj["poi_name"] = poi
                            obj["poi_id"] = obj["replied_to_user_id"]
                            json.dump(obj, f, ensure_ascii = False)
            if last_max_id == max_id or all(v >= 20 for v in replies_count_map.values()):
                break





        # for tweet_id in id_list:
        #     reply_count = 0
        #     RC=0
        #     print("Getting replies for tweet with id :"+str(tweet_id))
        #     for tweet in tweepy.Cursor(api.search, q='to:'+poi, since_id=tweet_id, max_id=None,count=1000,tweet_mode='extended').items(2000):
        #       i = i+1;
        #       if tweet.in_reply_to_status_id == tweet_id:
        #         print("Id of the reply is "+str(tweet.id))
        #         if reply_count <= 20 :
        #             RC+=1
        #             reply_count+=1
        #             replies_lis.append(tweet)
        #             with open(poi_replies_file, 'a+') as f:
        #                 obj = convertToObj(tweet)
        #                 obj["poi_name"] = poi
        #                 obj["poi_id"] = obj["replied_to_user_id"]
        #                 json.dump(obj, f)
        #         else:
        #             break

    except TweepError:
       time.sleep(10)
       extract_replies(poi,id_list,replies_lis,replies_count_map,max_id)

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

def convertToObj(tweet):
    obj={}
    obj["poi_name"] = tweet.user.screen_name
    obj["poi_id"] = tweet.user.id
    obj["verified"] = "true"
    obj["country"] = "India" ## fill these based on the POI ,may be have a map with country as value and poi as key written manually
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





min_date = datetime.datetime(2019, 9, 6)
max_date = datetime.datetime(2019, 9, 12)
poi = 'ombirlakota'
poi_tweet_file = poi + '--tweets.json'
poi_replies_file = poi + '-replies.json'
id_list = []
extract_tweets(poi,0,id_list)
time.sleep(1)
#id_list.append(1170120494017740801)
replies_list=[]
count_map = {}
print(len(id_list))
for id in id_list:
    count_map[id] = 0
extract_replies(poi,id_list,replies_list,count_map,0)

time.sleep(1)
# print('Original count', original_tweet)

# print('Filtered Replies count', filtered_count)
# print('Tot Replies count', RC, len(replies_list), list)

os.rename(poi + '--tweets.json', poi+'-tweets-replies-'+str(original_tweet)+'.json')