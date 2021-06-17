from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from pydantic import BaseModel
import tweepy, os
import json

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
def publicTweetsData(user):
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    # On inclue les retweets pour les calculs 
    publicTweets = api.user_timeline(user, count=200,include_rts=True)
    return publicTweets    

@app.get("/")
def index():
    return "Hello pip👋"

@app.get("/test/{user}")
def test(user):
    requeteData = publicTweetsData(user)
    pic = 0
    vid = 0
    
    data = requeteData[0]   

    ext_entities = data.extended_entities
    media = ext_entities["media"]
    _type = media[0]["_type"]
    if _type == "photo":
        pic += 1
    elif _type == "video":
        vid += 1
        infos = media[0]["video_info"]
    

@app.get("/pollutionIndirect/{user}")
def pollutionIndirect(data):

    requeteData = data
    # requeteData = publicTweetsData(user)

    average = Average(requeteData)
    averageLike = average["like"]
    averageRetweet = average["retweet"]

    user = requeteData[0].user
    posts = user.statuses_count

    pollution_Direct = pollutionDirect(requeteData)
    pollution_Direct = pollution_Direct["pollutionDirect"]

    moyPollutionParPost = pollution_Direct / posts

    pollution_Indirect = ((moyPollutionParPost * averageLike)+(moyPollutionParPost * averageRetweet)) * posts
    pollution_Indirect = int(pollution_Indirect)

    return {"pollution_Indirect": pollution_Indirect}


    
    

@app.get("/average/{user}")
def Average(data):
    # https://developer.twitter.com/en/docs/labs/tweet-metrics/api-reference/get-tweets-metrics
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    public_tweets = data
    likes = []
    retweets = []
    # Comments object is only available with the Premium and Enterprise tier products.

    i = 0

    for tweet in public_tweets:

        like = tweet.favorite_count
        likes.append(like)

        retweet = tweet.retweet_count
        retweets.append(retweet)

        i += 1
    somme = sum(likes)
    averageLike = somme / i
    averageLike = round(averageLike,1)

    sommeRetweets = sum(retweets)
    averageRetweet = sommeRetweets / i
    averageRetweet = round(averageRetweet,1)

    return {"like": averageLike, "retweet": averageRetweet}

# Séparer la pollution direct/indirect 

@app.get("/pollutionDirect/{user}")
def pollutionDirect(data):
    # Image size <= 5 MB, animated GIF size <= 15 MB
    requeteData = data
    pic = 0
    vid = 0
    txt = 0
    gif = 0
    totalCharacters = 0
    i = 0
    pollution1character = 0.001
    pollution1photo = 0.02
    pollutionParSecondeVid = 2
    vidSeconde = 0

    # likesSent = user.favourites_count

    user = requeteData[0].user
    # ext_entities = public_tweets.extended_entities
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/entities
    for tweet in requeteData:
        text = tweet.text
        totalCharacters += len(text)
        try:
            ext_entities = tweet.extended_entities
            media = ext_entities["media"]
            _type = media[0]["type"]
            
            if _type == "photo":
                pic += 1
            elif _type == "video":
                vid += 1
                infos = media[0]["video_info"]
                seconde = infos["duration_millis"] / 1000
                vidSeconde += seconde
            elif _type == "animated_gif":
                gif += 1
            else:
                break
        except:
            txt += 1
        i+=1
   
    moyenneTxt = txt/i
    moyenneVid = vid/i
    moyennePic = pic/i
    moyenneDuréeVid = 1
    moyenneCharactTxt = 1
    if vid != 0:
        moyenneDuréeVid = vidSeconde/vid

    if txt != 0:
        moyenneCharactTxt = totalCharacters/txt

    posts = user.statuses_count    

    totalSommes = (moyenneTxt * (moyenneCharactTxt * pollution1character)) + (moyennePic * pollution1photo) + (moyenneVid *(moyenneDuréeVid * pollutionParSecondeVid))
    pollutionDirect = totalSommes * posts
    pollutionDirect = int(pollutionDirect)

    return {"pollutionDirect":pollutionDirect, "moyenneTxt":moyenneTxt, "moyenneVid":moyenneVid, "moyennePic":moyennePic}


@app.get("/user/{user}")
def dataJson(user):
# 
    # / INFOS
    requeteData = publicTweetsData(user)
    username = user
    user = requeteData[0].user
    name = user.name
    surname = user.screen_name
    followers = user.followers_count
    profilePiclink = user.profile_image_url_https
    profilePic = profilePiclink.replace('_normal','')
    
    following = user.friends_count
    dateBegin = user.created_at
#
    # / POLLUTION
    # // DIRECT

    pollution_DirectData = pollutionDirect(requeteData)
    pollution_Direct = pollution_DirectData["pollutionDirect"]

    # // graphPollutionBySource

    moyText = pollution_DirectData["moyenneTxt"] * 100
    moyText = round(moyText,1)
    moyVid = pollution_DirectData["moyenneVid"] * 100
    moyVid = round(moyVid,2)
    moyPic = pollution_DirectData["moyennePic"] * 100
    moyPic = round(moyPic,1)

    sommeOutils = moyText + moyVid + moyPic
    moyGif = 100 - sommeOutils


    # // Indirect
    pollution_Indirect = pollutionIndirect(requeteData)
    pollution_Indirect = pollution_Indirect["pollution_Indirect"]

    sommePollutions = pollution_Indirect + pollution_Direct
   
    if sommePollutions == 0:
        sommePollutions = 1
    rapportIndirect = (pollution_Indirect * 100) / sommePollutions
    rapportIndirect = round(rapportIndirect,2)

    # // Score
    score = 0
    if sommePollutions < 10000:
        score += 30
        if pollution_Direct <= 100:
            score -= 15
        elif pollution_Direct >= 100 and pollution_Direct <= 250:
            score += 5
    elif sommePollutions >= 10000 and sommePollutions <= 5000:
        score += 70
        if pollution_Direct <= 100:
            score -= 15
        elif pollution_Direct >= 100 and pollution_Direct < 250:
            score += 5
    else:
        score += 100
        if pollution_Direct <= 100:
            score -= 15



    data = {
    "dataTwitter": [
        {
        "name": name,
        "surname": "@"+surname,
        "followers": followers,
        "profilPicUrl": profilePic,
        "following": following,
        }
    ],
    "dataEco":[
        {
        "score": score,

        "graphDirectPollution":[{
            "pollutionDirect":pollution_Direct,
            "seuilMax": 1000
        }],

        "graphRapportDirectIndirect":[{

            "pollutionDirect": pollution_Direct,
            "pollutionIndirect": pollution_Indirect,
            "rapport%": rapportIndirect
        }],

        "graphPollutionBySource":[{
            "text%": moyText,
            "video%": moyVid,
            "pic%": moyPic,
            "gif%": moyGif
        }],
        
        }
    ]
    }

    json_compatible_item_data = jsonable_encoder(data)

    return JSONResponse(content=json_compatible_item_data)