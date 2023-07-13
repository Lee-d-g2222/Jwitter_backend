from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)

    hearts = relationship("Heart", back_populates="tweet")
    retweets = relationship("Retweet", back_populates="tweet")
    user = relationship("User", back_populates="tweets")

class Heart(Base):
    __tablename__ = "hearts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tweet_id = Column(Integer, ForeignKey("tweets.id"))

    tweet = relationship("Tweet", back_populates="hearts")

class Retweet(Base):
    __tablename__ = "retweets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tweet_id = Column(Integer, ForeignKey("tweets.id"))

    tweet = relationship("Tweet", back_populates="retweets")

