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

@app.get("/average_like/{user}")
def average_like(user):
    # https://developer.twitter.com/en/docs/labs/tweet-metrics/api-reference/get-tweets-metrics
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    public_tweets = api.user_timeline(user, count=100,include_rts=False)
    likes = []
    i = 0
    for tweet in public_tweets:
        like = tweet.favorite_count
        likes.append(like)
        i += 1
    somme = sum(likes)
    averageLike = somme / i
    averageLike = int(averageLike)

    return averageLike

# Séparer la pollution direct/indirect 

@app.get("/pic/{user}")
def pic(user):
    # Image size <= 5 MB, animated GIF size <= 15 MB
    public_tweets = api.user_timeline(user, count=1)
    tweets = []
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/entities
    for tweet in public_tweets:
        media = tweet.entities["media"]
        tweets.append(media[0]["type"])

    return {"msg": tweets}
    



@app.get("/pollution/{user}")
def pollution(user):
# 
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    # / INFOS
    username = user
    user = api.get_user(user)
    name = user.name
    surname = user.screen_name
    followers = user.followers_count
    profilePic = user.profile_image_url_https
    following = user.friends_count
    dateBegin = user.created_at
#
    # / POLLUTION
    # // DIRECT

    averageLike = average_like(username)
    likesSent = user.favourites_count
    posts = user.statuses_count
    print(averageLike)


    
    return {
    "data-twitter": [
        {
        "NAME": name,
        "@surname": "@"+surname,
        "followers": followers,
        "profilPicURL": profilePic,
        "following": following,
    
        }
    ],
    "data-eco":[
        {
        "pollutionDirect":"2356",
        "pollutionIndirect":"10000",
        "text": "20",
        "video":"30",
        "image":"50",
        "score":"50"
        }
    ]
}

