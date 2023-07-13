from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Follow(Base):
    __tablename__ = "follow"

    follower_id = Column(Integer, ForeignKey("users.id"), primary_key=True) # 팔로우 하는 사람
    followed_id = Column(Integer, ForeignKey("users.id"), primary_key=True) # 팔로우 당하는 사람

    # 각각 follower 와 followed에 대한 relationship을 설정
    follower = relationship("User", foreign_keys=[follower_id], backref="following")
    followed = relationship("User", foreign_keys=[followed_id], backref="followers")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    nickname = Column(String, index=True)
    hashed_password = Column(String)

    is_auth_user = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    tweets = relationship("Tweet", back_populates="user")
    jwttokens = relationship("JwtToken", back_populates="user")

class JwtToken(Base):
    __tablename__ = "jwttokens"

    id = Column(Integer, primary_key=True, index=True)
    refresh_token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    user = relationship("User", back_populates="jwttokens")
