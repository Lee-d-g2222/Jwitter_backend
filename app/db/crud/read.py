from sqlalchemy.orm import Session
from app.db.schemas import user_schema
from app.db.models import tweet_model, user_model
from app.utils.hash import Hasher
from sqlalchemy import func, or_
from typing import List

async def get_user_by_login_id(db: Session, login_id: str):
    """
    username 또는 email로 User를 DB에서 찾는 함수
    """
    user = db.query(user_model.User).filter(
        or_(user_model.User.username == login_id, user_model.User.email == login_id)
    ).first()
    if user:
        return user
    return False

async def verify_refresh_token(db: Session, refresh_token: str, user_id: int):
    """
    refresh token이 유효한지 확인하는 함수
    """
    token_db = db.query(user_model.JwtToken).filter(user_model.JwtToken.user_id == user_id).first()
    # 바이트 문자열로 저장되어있는 토큰을 디코딩하여 문자열로 변환
    decoded_token = token_db.refresh_token.decode('utf-8')
    if decoded_token == refresh_token:
        return True
    return False

async def verify_user(db: Session, user: user_schema.UserLogin):
    db_user = await get_user_by_login_id(db, user.id)
    if db_user:
        if Hasher.verify_hashed_text(plain_password=user.password, hashed_text=db_user.hashed_password):
            return db_user
    return False

async def get_user_by_user_id(db: Session, user_id: int):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if user:
        return user
    return False

async def get_tweets_from_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(tweet_model.Tweet)
        .filter(tweet_model.Tweet.author_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def count_hearts(db: Session, tweet_ids: List[int]):
    results = db.query(tweet_model.Heart.tweet_id, func.count(tweet_model.Heart.id)).filter(tweet_model.Heart.tweet_id.in_(tweet_ids)).group_by(tweet_model.Heart.tweet_id).all()
    return dict(results)

def count_retweets(db: Session, tweet_ids: List[int]):
    results = (
        db.query(tweet_model.Tweet.id, func.count(tweet_model.Retweet.id))
        .join(tweet_model.Retweet)  # "retweets"와 "tweets" 테이블을 연결합니다.
        .filter(tweet_model.Retweet.tweet_id.in_(tweet_ids))
        .group_by(tweet_model.Tweet.id)
        .all()
    )
    return dict(results)


async def count_hearts_and_retweets(db: Session, tweet_ids: List[int]):
    heart_counts = count_hearts(db, tweet_ids)
    retweet_counts = count_retweets(db, tweet_ids)
    return heart_counts, retweet_counts



async def get_follower_count(db: Session, user_id: int):
    return db.query(user_model.Follow).filter(user_model.Follow.followed_id == user_id).count()

async def get_following_count(db: Session, user_id: int):
    return db.query(user_model.Follow).filter(user_model.Follow.follower_id == user_id).count()
