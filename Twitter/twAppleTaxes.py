import sys
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import datetime
import json

reload(sys)
sys.setdefaultencoding('utf8')

def getTimeStr():
    return str(datetime.datetime.now().time())

class MyListener(StreamListener):

    count_Android = 0
    count_iPhone = 0

    def __init__(self, query):
        self.outfile = "stream_%s.json" % (query)

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                tw = json.loads(data)
                type = 0
                if ("Twitter for iPhone" in tw['source']):
                    type = 1
                    self.count_iPhone += 1
                elif ("Twitter for Android" in tw['source']):
                    type = 2
                    self.count_Android += 1

                if (type > 0):
                    TABS = "\t"
                    out = "iPhone" if type == 1 else "Android"
                    out += TABS + tw['text'].replace('\n',' ').replace('\r','').replace('\t',' ').encode('utf-8')
                    out += TABS + "@" + tw['user']['screen_name']
                    out += TABS + getTimeStr() + TABS
                    out += "i" + str(self.count_iPhone) if type == 1 else "a" + str(self.count_Android)
                    out += "\n"
                    f.write(out)
                    print out
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True

# Twitter dev credentials
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your-access_token'
access_secret = 'access_secret'

if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    print "-Start: " + str(datetime.datetime.now().time())

    search = u"#AppleTax"
    twitter_stream = Stream(auth, MyListener(search))
    twitter_stream.filter(track=[search])