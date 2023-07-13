from sqlalchemy.orm import Session
from app.db.models import tweet_model, user_model
from sqlalchemy import and_
from fastapi import HTTPException
from app.db.crud.read import get_user_by_user_id

async def delete_refresh_token_by_userId(db: Session, user_id: int):
    existing_token = db.query(user_model.JwtToken).filter(user_model.JwtToken.user_id == user_id).first()
    if existing_token:
        db.delete(existing_token)
        db.commit()
        return True
    return False

async def delete_tweet(db: Session, tweet_id: int, user_id: int):
    existing_tweet = db.query(tweet_model.Tweet).filter_by(id=tweet_id).first()
    if existing_tweet and existing_tweet.author_id == user_id:
        db.delete(existing_tweet)
        db.commit()
        return True
    return False

async def unfollow_user(db: Session, user_id: int, followed_id: int):
    # user_id : 언팔로우 하는 사람 : follower
    # followed_id : 언팔로우 당하는 사람 : following
    if await get_user_by_user_id(db, user_id):
        print(1)
        is_followed = db.query(user_model.Follow).filter(and_(user_model.Follow.follower_id == user_id, user_model.Follow.followed_id == followed_id)).first()
        print(is_followed)
        if is_followed:
            db.delete(is_followed)
            db.commit()
            return True
        else:
            raise HTTPException(status_code=409, detail="Not followed")
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
async def delete_heart(db: Session, tweet_id: int, user_id: int):
    is_tweet = db.query(tweet_model.Tweet).filter(tweet_model.Tweet.id == tweet_id).first()
    if is_tweet:
        is_hearted = db.query(tweet_model.Heart).filter(and_(tweet_model.Heart.user_id == user_id, tweet_model.Heart.tweet_id == tweet_id)).first()
        if is_hearted:
            db.delete(is_hearted)
            db.commit()
            return True
        else:
            raise HTTPException(status_code=409, detail="Not hearted")

async def delete_retweet(db: Session, tweet_id: int, user_id: int):
    is_tweet = db.query(tweet_model.Tweet).filter(tweet_model.Tweet.id == tweet_id).first()
    if is_tweet:
        is_retweeted = db.query(tweet_model.Retweet).filter(and_(tweet_model.Retweet.user_id == user_id, tweet_model.Retweet.tweet_id == tweet_id)).first()
        if is_retweeted:
            db.delete(is_retweeted)
            db.commit()
            return True
        else:
            raise HTTPException(status_code=409, detail="Not retweeted")