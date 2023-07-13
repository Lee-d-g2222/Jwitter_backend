from fastapi import APIRouter
from app.api import users, tweets, follows
from app.core.config import Settings


router = APIRouter()

router.include_router(users.router, tags=["users"], prefix="/users")
router.include_router(tweets.router, tags=["tweets"], prefix="/tweets")
router.include_router(follows.router, tags=["follow"], prefix="/users")