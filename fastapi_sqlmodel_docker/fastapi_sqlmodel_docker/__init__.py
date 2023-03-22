from fastapi import FastAPI, Depends, HTTPException
from transformers import pipeline
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from UserInDB import UserInDB
from User import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union
from contextlib import asynccontextmanager
import os, dotenv
from jose import JWTError, jwt


translator_models = {}
# Load environment variables
dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer("/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


authorized_users = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": os.getenv("PASSWORD"),
        "disabled": False,
    }
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the translation models
    translator_models["model1"] = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")
    translator_models["model2"] = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en")
    yield
    # Clean up the models and release the resources
    translator_models.clear()

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)
    return []


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return user


def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expire is None:
        expires = datetime.utcnow() + timedelta(minutes=15)
    else:
        expires = datetime.utcnow() + time_expire
    data_copy.update({"exp": expires})
    token_jwt = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = token_decode.get("sub")
        if username == None:
            raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    user = get_user(authorized_users, username)
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    return user


def get_user_disable_current(user: User = Depends(get_current_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


def model1_en_es(text: str) -> str:
    return translator_models["model1"](text)[0]['translation_text']


def model2_es_en(text: str) -> str:
    return translator_models["model2"](text)[0]['translation_text']


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"Message": "Hello World"}

@app.get("/users/me")
async def user(user: User = Depends(get_user_disable_current)):
    return user

@app.get("/translation-en-es/{text}")
async def translation_model1(text: str, token: str = Depends(oauth2_scheme)):
    return {"English to Spanish": model1_en_es(text)}

@app.get("/translation-es-en/{text}")
async def translation_model2(text: str, token: str = Depends(oauth2_scheme)):
    return {"Spanish to English": model2_es_en(text)}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(authorized_users, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_token({"sub": user.username}, access_token_expires)

    return {
        "access_token": access_token_jwt,
        "token_type": "bearer",
    }