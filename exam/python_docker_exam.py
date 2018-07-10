import nltk
from geopy import Nominatim
from nltk.corpus import stopwords
from tweepy.streaming import StreamListener, json
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
import time

nltk.download('stopwords')
STOP_WORDS = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about',
              'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be',
              'some', 'for', 'do', 'its', 'yours', 'de', 'vs', 'such', 'into', 'of', 'most', 'itself',
              'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each',
              'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his',
              'through', 'don', '\'\'', 'nor', 'me', 'were', 'her', 'more', 'himself',
              'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both',
              'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any',
              'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on',
              'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why',
              'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has',
              'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after',
              'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by',
              'doing', 'it', 'how', 'further', 'was', 'here', 'than', 'The',
              'rt', '&amp', ' ', '', '``', 'http', 'via', 'https', 'amp', '\'s']
STOP_WORDS = set(stopwords.words('english') + STOP_WORDS)
WORD_TO_TRACK = ['worldcup']

WORD_TOKENIZER = nltk.RegexpTokenizer('[a-zA-Z]\w+')

TWITTER_VAR = {
    "consumer_key": u'5KHfdzjZpsSef0pDjHSIUqxkb',
    "consumer_secret": u'HiKeFDDaYK1iY3R3nnRVZOfPVDNuYySm0MXDYV2kS878xIAvSP',
    "access_token": u'762963428973617152-snH3bENqYdoN4MRi8d02GrxFUO9Gi1O',
    "access_token_secret": u'COoonSphtHDQtcArpdJbg1q0CLozML4yZS91pbenuk5yL'}

MONGO_VAR = {
    "dbuser": 'sharonhadar',
    "dbpassword": 'Aa123456',
    "dbname": 'sharonhadar_db',
    "host": 'ds125381.mlab.com',
    "port": 25381}


def connect_to_db():
    # Connect to mongo data base
    connection = pymongo.MongoClient(MONGO_VAR["host"], MONGO_VAR["port"])
    db = connection[MONGO_VAR["dbname"]]
    db.authenticate(MONGO_VAR["dbuser"], MONGO_VAR["dbpassword"])
    print('db', db)
    return db, connection


class StdOutListener(StreamListener):
    twitts_db, connection = connect_to_db()
    TWIT_BY_LOCATION = twitts_db.twit_exam

    def __init__(self):
        super().__init__()

    def on_data(self, data):
        twit = json.loads(data)
        if "user" in twit and "location" in twit["user"] and twit["user"]["location"]:
            self.add_words_to_mongo(twit)
        return True

    def on_error(self, status):
        # close all MongoDB
        self.connection.close()
        print("terminated.")

    @staticmethod
    def tokenize_tweet_text(tweet_text):
        word_tokens = WORD_TOKENIZER.tokenize(tweet_text)
        filtered_sentence = []
        for w in word_tokens:
            if len(w) > 1 and w.lower() not in STOP_WORDS:
                w = nltk.re.sub('[!@#$]', '', w)
                filtered_sentence.append(w.lower())
        return filtered_sentence

    def add_words_to_mongo(self, twit):
        text = twit["text"]

        tokens = self.tokenize_tweet_text(text)
        for token in tokens:
            post_id = self.TWIT_BY_LOCATION.find_one_and_update(
                {'token': token},
                {'$inc': {"count": 1}},
                upsert=True)
            print("post_id: ", post_id)


if __name__ == '__main__':
    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(TWITTER_VAR["consumer_key"], TWITTER_VAR["consumer_secret"])
    auth.set_access_token(TWITTER_VAR["access_token"], TWITTER_VAR["access_token_secret"])

    i = 0
    while i < 10:
        try:
            stream = Stream(auth, l)
            stream.filter(track=WORD_TO_TRACK)
        except:
            print("restarting")
            time.sleep(3)
            i += 1
    print("exit process")
