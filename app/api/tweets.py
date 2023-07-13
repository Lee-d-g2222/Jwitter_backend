from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.schemas import tweet_schema, user_schema
from app.db.crud import create, read, update, delete
from app.utils.jwt import JWT
from typing import List, Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter()

@router.get("/me", response_model=tweet_schema.TweetResponse)
async def read_user_tweets(
                        db: Session = Depends(get_db), 
                        token: Annotated[str, Depends(oauth2_scheme)] = None, 
                        skip: int = 0, 
                        limit: int = 10
                        ):
    subject = JWT.verify_access_token_and_get_sub(token)
    tweets_db = await read.get_tweets_from_user_id(db, subject, skip, limit)
    tweets = []

    if tweets_db:
        tweet_ids = [tweet_db.id for tweet_db in tweets_db]
        heart_counts, retweet_counts = await read.count_hearts_and_retweets(db, tweet_ids)

        for tweet_db in tweets_db:
            tweet = tweet_schema.Tweet(
                tweet_id=tweet_db.id,
                user_id=subject,
                nickname=tweet_db.user.nickname,
                username=tweet_db.user.username,
                content=tweet_db.content,
                hearts=heart_counts.get(tweet_db.id, 0),
                retweets=retweet_counts.get(tweet_db.id, 0)
            )
            tweets.append(tweet)
    temp = tweet_schema.TweetResponse(
        tweets=tweets
    )
    return temp


@router.post("/create")
async def create_tweet(tweet: tweet_schema.TweetCreate, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_access_token_and_get_sub(token)
    tweet_db = await create.create_tweet(db, tweet.content, subject)

    if not tweet_db:
        raise HTTPException(status_code=404, detail="Tweet not created")
    return {
        "id" : tweet_db.id,
        "username" : tweet_db.user.username,
        "nickname" : tweet_db.user.nickname,
        "content" : tweet_db.content
    }

@router.put("/update")
async def update_tweet(tweet: tweet_schema.TweetUpdate, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_access_token_and_get_sub(token)

    if await update.update_tweet(db, tweet, subject):
        raise HTTPException(status_code=200, detail="Tweet updated")
    raise HTTPException(status_code=404, detail="Tweet not Found")
    

@router.delete("/delete")
async def delete_tweet(tweet_id: int, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_access_token(token)

    if await delete.delete_tweet(db, tweet_id, subject):
        raise HTTPException(status_code=200, detail="Tweet deleted")
    raise HTTPException(status_code=404, detail="Tweet not Found")

@router.post("/add/heart")
async def add_heart(tweet_id: int, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_access_token_and_get_sub(token)

    if await create.add_heart(db, tweet_id, subject):
        raise HTTPException(status_code=200, detail="Heart added")
    raise HTTPException(status_code=404, detail="Tweet not Found")

@router.post("/add/retweet")
async def add_retweet(tweet_id: int, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_access_token_and_get_sub(token)

    if await create.add_retweet(db, tweet_id, subject):
        raise HTTPException(status_code=200, detail="Retweet added")
    raise HTTPException(status_code=404, detail="Tweet not Found")

@router.delete("/delete/heart")
async def delete_heart(tweet_id: int, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_access_token_and_get_sub(token)

    if await delete.delete_heart(db, tweet_id, subject):
        raise HTTPException(status_code=200, detail="Heart deleted")
    raise HTTPException(status_code=404, detail="Tweet not Found")

@router.delete("/delete/retweet")
async def delete_retweet(tweet_id: int, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_access_token_and_get_sub(token)

    if await delete.delete_retweet(db, tweet_id, subject):
        raise HTTPException(status_code=200, detail="Retweet deleted")
    raise HTTPException(status_code=404, detail="Tweet not Found")
