from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# Enable CORS so frontend can communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

quotes = [
    "Life is what happens when you're busy making other plans.",
    "Strive not to be a success, but rather to be of value.",
    "The best way to predict the future is to create it.",
    "Do not watch the clock. Do what it does. Keep going.",
]

@app.get("/quote")
async def get_quote():
    return {"quote": random.choice(quotes)}
