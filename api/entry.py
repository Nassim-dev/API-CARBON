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

# Specifies the number of Tweets to try and retrieve, up to a maximum of 200 per distinct request
# Returns recent Tweets posted
def public_Tweets(user):
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    public_tweets = api.user_timeline(user, count=200,include_rts=False)
    return public_tweets

@app.get("/")
def index():
    return "Hello pip👋"

@app.get("/users/{user}")
def read_root(user):
    public_tweets = public_Tweets(user)
    tweets = []
    print(public_tweets)
    i = 0
    for tweet in public_tweets:
        tweets.append(tweet.text)
        i += 1
    print(i)
    return {"msg": tweets}

@app.get("/followers/{user}")
def follow_user(user):
    user = api.get_user(user)
    followers = user.followers_count
    return {"followers": followers}

@app.get("/average/{user}")
def Average(user):
    # https://developer.twitter.com/en/docs/labs/tweet-metrics/api-reference/get-tweets-metrics
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    public_tweets = public_Tweets(user)
    likes = []
    retweets = []
    # Comments object is only available with the Premium and Enterprise tier products.

    pics = 0
    texts = 0
    videos = 0

    i = 0
    for tweet in public_tweets:

        like = tweet.favorite_count
        likes.append(like)

        retweet = tweet.retweet_count
        retweets.append(retweet)

        i += 1
    somme = sum(likes)
    averageLike = somme / i
    averageLike = int(averageLike)

    sommeRetweets = sum(retweets)
    averageRetweet = sommeRetweets / i
    averageRetweet = int(averageRetweet)

    return {"like": averageLike, "retweet": averageRetweet}

# Séparer la pollution direct/indirect 

@app.get("/pic/{user}")
def pic(user):
    # Image size <= 5 MB, animated GIF size <= 15 MB
    public_tweets = api.user_timeline(user, count=4)
    pic = 0
    vid = 0
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/entities
    for tweet in public_tweets:
        media = tweet.entities["media"]
        type = media[0]["type"]

        if type == "photo":
            pic += 1
        elif type == "video":
            vid += 1
        

    return {"numberPic": pic}

@app.get("/pollution_direct/{user}")
def pollution_direct(user):
    
    user = api.get_user(user)
    numbersPost = user.statuses_count
    return numbersPost

    



@app.get("/pollution/{user}")
def pollution(user):
# 
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

    average = Average(username)
    averageLike = average["like"]
    averageRetweet = average["retweet"]
    likesSent = user.favourites_count
    posts = user.statuses_count
    print(averageLike)


    
    return {
    "data-twitter": [
        {
        "name": name,
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

