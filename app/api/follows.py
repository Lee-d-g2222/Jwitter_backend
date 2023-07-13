from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud import create, read, update, delete
from app.utils.jwt import JWT
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter()

@router.post("/follow")
async def follow_user(
            following_id: int, 
            db: Session = Depends(get_db), 
            token: Annotated[str, Depends(oauth2_scheme)] = None
            ):    
    subject = JWT.verify_access_token_and_get_sub(token)

    if subject == following_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")
    
    await create.follow_user(db, subject, following_id)
    raise HTTPException(status_code=200, detail="Successfully followed")

@router.delete("/unfollow")
async def unfollow_user(
            followed_id: int, 
            db: Session = Depends(get_db),
            token: Annotated[str, Depends(oauth2_scheme)] = None
            ):
    subject = JWT.verify_access_token_and_get_sub(token)

    if subject == followed_id:
        raise HTTPException(status_code=400, detail="You cannot unfollow yourself")
    print(3)
    await delete.unfollow_user(db, subject, followed_id)
    raise HTTPException(status_code=200, detail="Successfully unfollowed")