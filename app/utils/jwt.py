import jwt
from datetime import datetime, timedelta
from app.core.config import get_settings
from fastapi import HTTPException

class JWT:
    @staticmethod
    def create_access_token(subject: str, expires_delta: timedelta = None):
        expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
        payload = { "sub": subject, "exp": expire }

        settings = get_settings()
        encoded_jwt = jwt.encode(payload, settings.access_secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(subject: str):   
        payload = { "sub": subject, "exp": datetime.utcnow() + timedelta(days=7) }
        settings = get_settings()
        encoded_jwt = jwt.encode(payload, settings.refresh_secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    @staticmethod
    def verify_access_token_and_get_sub(token: str):
        return JWT.verify_access_token(token).get('sub')

    @staticmethod
    def verify_refresh_token_and_get_sub(token: str):
        return JWT.verify_refresh_token(token).get('sub')

    @staticmethod
    def verify_access_token(token: str):
        settings = get_settings()
        try:
            payload = jwt.decode(
                token,
                settings.access_secret_key,
                algorithms=[settings.algorithm]
            )
            exp = payload.get('exp')
            if exp is None or datetime.utcfromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(status_code=401, detail="Token has expired")
            return payload
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
    @staticmethod
    def verify_refresh_token(token: str):
        settings = get_settings()
        try:
            payload = jwt.decode(
                token,
                settings.refresh_secret_key,
                algorithms=[settings.algorithm]
            )
            exp = payload.get('exp')
            if exp is None or datetime.utcfromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(status_code=401, detail="Token has expired")
            return payload
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")