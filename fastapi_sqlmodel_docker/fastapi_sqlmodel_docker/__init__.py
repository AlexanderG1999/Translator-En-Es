from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from transformers import pipeline


def model1_en_es(text: str) -> str:
    model_checkpoint = "Helsinki-NLP/opus-mt-en-es"
    translator = pipeline("translation", model=model_checkpoint)
    return translator(text)[0]['translation_text']

def model2_es_en(text: str) -> str:
    model_checkpoint = "Helsinki-NLP/opus-mt-es-en"
    translator = pipeline("translation", model=model_checkpoint)
    return translator(text)[0]['translation_text']

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    pages: int
    editorial: Optional[str]

#http://127.0.0.1:8000

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/books/{id}")
def show_book(id: int):
    return {"id": id}

@app.post("/books")
def insert_book(book: Book):
    return {"message": f"libro {book.title} insertado"}

@app.get("/translation-en-es/{text}")
def translation_model1(text: str):
    return {"English to Spanish": model1_en_es(text)}

@app.get("/translation-es-en/{text}")
def translation_model2(text: str):
    return {"Spanish to English": model2_es_en(text)}