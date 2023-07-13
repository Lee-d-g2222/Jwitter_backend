from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher():
    @staticmethod
    def verify_hashed_text(plain_password : str, hashed_text : str):
        return pwd_context.verify(plain_password, hashed_text)

    @staticmethod
    def hashing(plain_text : str):
        return pwd_context.hash(plain_text)
