
# tweeter data mining task1 one solution  date: 17 july 2017
# jay harer

import tweepy
from tweepy import OAuthHandler
import json

consumer_key = "BKxdUMU17lNsCM5qsjbjUqUl6"
consumer_secret = "3WKT79JyDTcxsrrFlXXpWG93TNwkfNAuactNCodaEF8iLaRhzR"
access_token = "885097450842669060-HVscWKB97he4V8rHveG7pk1c2Kx2TTZ"
access_secret = "OvenhFgyFM4VtQEeEuCQGFZje5b1w22XffuXf8QPMnakd"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

try:
  f = open("tweet_data.json","a") 

# all tweets from home user
  public_tweets = api.home_timeline()
  for tweet in public_tweets:
    s=json.dumps(tweet._json)  # convert dict format into json string
    f.write(s)                 # write tweets into json file
    print(tweet._json)


 # tweets from specific user
  tweet_data = api.user_timeline(id="jay harer", count=20)
  for tweet in tweet_data:
    s = json.dumps(tweet._json)
    f.write(s)
    print(tweet._json)


# tweets by search keyword
  results = api.search(q="feedback", lang="en")
  for tweet in results:
    s = json.dumps(tweet._json)
    f.write(s)
    print(tweet._json)

except IOError:
  print("error in writing file tweet_data.json")
  f.close()

else:
    print("ok successfuly write into file tweet_data.json")

