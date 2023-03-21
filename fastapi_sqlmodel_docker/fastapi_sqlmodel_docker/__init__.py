from fastapi import FastAPI, Depends, HTTPException
from transformers import pipeline
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from UserInDB import UserInDB
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union
from contextlib import asynccontextmanager
#from jose import JWTError, jwt

authorized_users = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2a$12$F0xqCui75b8yXvi42J6PFuIAHXhBryMjDE/3OwLxyPDB91FyrLEzq",
        "disabled": False,
    }
}

#SECRET_KEY = "secret_key"
#ALGORITHM = "HS256"
translator_models = {}

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
        raise HTTPException(status_code=400, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return user


'''def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expire is None:
        expires = datetime.utcnow() + timedelta(minutes=15)
    else:
        expires = datetime.utcnow() + time_expire
    data_copy.update({"exp": expires})
    token_jwt = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt'''


def model1_en_es(text: str) -> str:
    return translator_models["model1"](text)[0]['translation_text']


def model2_es_en(text: str) -> str:
    return translator_models["model2"](text)[0]['translation_text']


app = FastAPI(lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer("/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/")
async def root():
    return {"Message": "Hello World"}

@app.get("/users/me")
async def user_me(token: str = Depends(oauth2_scheme)):
    return "I am an User"

@app.get("/translation-en-es/{text}")
async def translation_model1(text: str, token: str = Depends(oauth2_scheme)):
    return {"English to Spanish": model1_en_es(text)}

@app.get("/translation-es-en/{text}")
async def translation_model2(text: str, token: str = Depends(oauth2_scheme)):
    return {"Spanish to English": model2_es_en(text)}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(authorized_users, form_data.username, form_data.password)
    #access_token_expires = timedelta(minutes=30)
    #access_token_jwt = create_token({"sub": user.username}, access_token_expires)

    return {
        "access_token": "fake-jwt-token",
        "token_type": "bearer",
    }