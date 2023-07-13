from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.db.schemas import user_schema, tweet_schema
from app.db.models import tweet_model, user_model
from app.utils.hash import Hasher
from app.db.crud.read import get_user_by_user_id

async def add_to_db(db: Session, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance

async def create_user(db: Session, user: user_schema.UserCreate):
    # 유저네임 & 이메일 중복 확인
    existing_user = db.query(user_model.User).filter(
        or_(user_model.User.username == user.username, user_model.User.email == user.email)
    ).first()
    # 중복이 아니면 DB에 추가
    if not existing_user:
        hashed_password = Hasher.hashing(user.password)
        db_user = user_model.User(email=user.email, username=user.username, nickname=user.nickname, hashed_password=hashed_password)
        if await add_to_db(db, db_user):
            return db_user
    return False

        
async def add_refresh_token(db: Session, refresh_token: str, user_id: int):
    db_refresh_token = user_model.JwtToken(refresh_token=refresh_token, user_id=user_id)
    if await add_to_db(db, db_refresh_token):
        return True
    return False
    
    
async def create_tweet(db: Session, content: str, user_id: int):
    db_tweet = tweet_model.Tweet(content=content, author_id=user_id)
    if await add_to_db(db, db_tweet):
        return db_tweet
    return False

async def follow_user(db: Session, user_id: int, follow_id: int):
    # user_id : 팔로우 하는 사람 : follower
    # follow_id : 팔로우 당하는 사람 : following
    if await get_user_by_user_id(db, user_id):
        is_followed = db.query(user_model.Follow).filter(and_(user_model.Follow.follower_id == user_id, user_model.Follow.followed_id == follow_id)).first()
        print(is_followed)
        if is_followed:
            raise HTTPException(status_code=409, detail="Already followed")
        else:
            db_follow = user_model.Follow(follower_id=user_id, followed_id=follow_id)
            if await add_to_db(db, db_follow):
                return db_follow
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
async def add_heart(db: Session, tweet_id: int, user_id: int):
    db_tweet = db.query(tweet_model.Tweet).filter(tweet_model.Tweet.id == tweet_id).first()
    if db_tweet:
        db_heart = db.query(tweet_model.Heart).filter(and_(tweet_model.Heart.tweet_id == tweet_id, tweet_model.Heart.user_id == user_id)).first()
        if db_heart:
            raise HTTPException(status_code=409, detail="Already hearted")
        else:
            db_heart = tweet_model.Heart(user_id=user_id, tweet_id=tweet_id)
            return await add_to_db(db, db_heart)
    else:
        raise HTTPException(status_code=404, detail="Tweet not found")

async def add_retweet(db: Session, tweet_id: int, user_id: int):
    db_tweet = db.query(tweet_model.Tweet).filter(tweet_model.Tweet.id == tweet_id).first()
    if db_tweet:
        db_retweet = db.query(tweet_model.Retweet).filter(and_(tweet_model.Retweet.tweet_id == tweet_id, tweet_model.Retweet.user_id == user_id)).first()
        if db_retweet:
            raise HTTPException(status_code=409, detail="Already retweeted")
        else:
            db_retweet = tweet_model.Retweet(user_id=user_id, tweet_id=tweet_id)
            return await add_to_db(db, db_retweet)
    else:
        raise HTTPException(status_code=404, detail="Tweet not found")