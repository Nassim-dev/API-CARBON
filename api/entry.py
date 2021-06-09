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

api = tweepy.API(auth, wait_on_rate_limit=True)

# NAssim

@app.get("/")
def index():
    return "Hello pip👋"

@app.get("/users/{user}")
def read_root(user):
    public_tweets = api.user_timeline(user, count=3)
    tweets = []
    for tweet in public_tweets:
        tweets.append(tweet.text)
    return {"msg": tweets}

@app.get("/followers/{user}")
def follow_user(user):
    user = api.get_user(user)
    followers = user.followers_count
    return {"followers": followers}

@app.get("/post/{user}")
def post_user(user):
    # https://developer.twitter.com/en/docs/labs/tweet-metrics/api-reference/get-tweets-metrics
    public_tweets = api.user_timeline(user, count=100,include_rts=False)
    tweets = []
    i = 0
    for tweet in public_tweets:
        tweet = tweet.id
        status = api.get_status(tweet)
        favorite_count = status.favorite_count
        if favorite_count != 0:
            tweets.append(favorite_count)
        i += 1
    somme = sum(tweets)
    averageLike = somme / i
    print(int(averageLike))

    return tweets, i


@app.get("/numberlikes/{user}")
def number_user_liked_sendes(user):
    user = api.get_user(user)
    likes = user.favourites_count

    return {"likes": likes}

# Séparer la pollution direct/indirect 



@app.get("/pic/{user}")
def pic(user):
# Image size <= 5 MB, animated GIF size <= 15 MB

    public_tweets = api.user_timeline(user, count=1)
    tweets = []

    i = 0
    for tweet in public_tweets:
        media = tweet.entities["media"]
        tweets.append(media[0]["type"])

    return {"msg": tweets}
    
# https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/entities


@app.get("/pollution/{user}")
def pollution_direct(user):
# 
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    # / INFOS
    user = api.get_user(user)
    name = user.name
    surname = user.screen_name
    followers = user.followers_count
    profilePic = user.profile_image_url_https
    dateBegin = user.created_at
    
#
    # / POLLUTION
    # // DIRECT

    likes = user.favourites_count
    posts = user.statuses_count
    print(likes,posts)

    


    return {
        # INFOS
        "NAME": name,
        "@surname": "@"+surname,
        "followers": followers,
        "profilPicURL": profilePic,
        "dateBegin": dateBegin,
    #####################
        # POLLUTION
        # // DIRECT


    }

