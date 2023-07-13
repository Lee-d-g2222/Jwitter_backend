from sqlalchemy.orm import Session
from app.db.models import tweet_model, user_model
from app.db.schemas import tweet_schema

# ※ UPDATE QUERY ※

async def update_tweet(db: Session, tweet: tweet_schema.TweetUpdate, user_id: int):
    user_db = db.query(tweet_model.Tweet).filter_by(id=tweet.tweet_id).first()
    if user_db and user_db.author_id == user_id:
        user_db.content = tweet.content
        db.commit()
        db.refresh(user_db)
        return True
    return False

async def update_user_nickname(db: Session, nickname: str, user_id: int):
    user_db = db.query(user_model.User).filter_by(user_id=user_id).first()
    if user_db:
        user_db.nickname = nickname
        db.commit()
        db.refresh(user_db)
        return True
    return False