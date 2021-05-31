from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import tweepy

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


auth = tweepy.AppAuthHandler("ynLU7uJVRqWAmiqPdw8KSqxPu", "IByfALAjERVHR3Cr9pXp2eUkihyFimgOiyynR7DL0XDrvVjfHx")
api = tweepy.API(auth)


@app.get("/{user}")
def read_root(user):
    public_tweets = api.user_timeline(user, count=10)
    tweets = []
    for tweet in public_tweets:
        tweets.append(tweet.text)
    return {"msg": tweets}
