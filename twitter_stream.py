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
WORD_TO_TRACK = ['world']

WORD_TOKENIZER = nltk.RegexpTokenizer('[a-zA-Z]\w+')

TWITTER_VAR = {
    "consumer_key": u'X',
    "consumer_secret": u'X',
    "access_token": u'X-X',
    "access_token_secret": u'X'}

MONGO_VAR = {
    "dbuser": 'X',
    "dbpassword": 'X',
    "dbname": 'X',
    "host": 'X',
    "port": X}


def connect_to_db():
    # Connect to mongo data base
    connection = pymongo.MongoClient(MONGO_VAR["host"], MONGO_VAR["port"])
    db = connection[MONGO_VAR["dbname"]]
    db.authenticate(MONGO_VAR["dbuser"], MONGO_VAR["dbpassword"])
    print('db', db)
    return db, connection


class StdOutListener(StreamListener):
    twitts_db, connection = connect_to_db()
    TWIT_BY_LOCATION = twitts_db.twit_by_location
    GEOLOCATOR = Nominatim()
    DEFAULT_LOCATION = "NY"

    def __init__(self):
        super().__init__()
        location_name = self.get_not_taken_location()
        if location_name is None:
            location_name = self.DEFAULT_LOCATION
        self.location = self.get_coord(location_name)

    @classmethod
    def get_coord(cls, location="New york", i=3):
        try:
            location = cls.GEOLOCATOR.geocode(location, addressdetails=True)
            return location.raw['address']["country"]
        except:
            if i >= 0:
                print("retry getting location name for time:", 3 - i)
                return cls.get_coord(location=location, i=i - 1)
            else:
                print("could not find location: ", location)
                return None

    def get_not_taken_location(self):
        locations = self.twitts_db['locations']
        cursor = self.twitts_db.locations.find({"isTaken": 0})
        my_doc = None

        for doc in cursor:
            my_doc = doc
            break

        if my_doc is None:
            print("NOTICE: all locations are taken!! using default location")
            return None

        my_location = my_doc['location']
        query = {'location': my_location}
        locations.update_one(query, {'$set': {'isTaken': 1}})
        return my_location

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
        location = self.get_coord(twit["user"]["location"])

        if location is None or location != self.location:
            return

        tokens = self.tokenize_tweet_text(text)
        for token in tokens:
            post_id = self.TWIT_BY_LOCATION.find_one_and_update(
                {'token': token, "location": location},
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
