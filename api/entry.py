from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import tweepy, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


auth = tweepy.AppAuthHandler(
    os.environ.get('TWITTER_API_KEY'), 
    os.environ.get('TWITTER_SECRET_KEY')
)

api = tweepy.API(auth)

# NAssim

@app.get("/users/{user}")
def read_root(user):
    public_tweets = api.user_timeline(user, count=10)
    tweets = []
    for tweet in public_tweets:
        tweets.append(tweet.text)
    return {"msg": tweets}

@app.get("/")
def index():
    return "Hello  👋"
