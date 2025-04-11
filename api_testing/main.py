from fastapi import FastAPI
import random

app = FastAPI()

side_hustles = [

    # Online Side Hustles
    "Freelance Web Development",
    "Content Creation",
    "Graphic Design",
    "Online Tutoring",
    "Affiliate Marketing",
    "Dropshipping",
    "Virtual Assistant",
    "Social Media Management",
    "UI/UX Design",
    "Stock Photography",

    # Tech-Related Side Hustles
    "App Development",
    "Data Analysis Services",
    "SEO Consulting",
    "Coding Courses",
    "Game Development",

    # Creative Side Hustles
    "Etsy Shop",
    "Print on Demand",
    "Voice Acting",
    "Music Production",
    "Photography Business",

    # Service-Based Side Hustles
    "Event Planning",
    "Pet Sitting/Dog Walking",
    "Home Cleaning Services",
    "Personal Training",
    "Handyman Services",

    # Passive Income Ideas
    "E-book Publishing",
    "Real Estate Investing",
    "Stock/Dividend Investing",
    "Creating Online Courses",
    "YouTube Automation"
]


money_quotes = [
    "Money often costs too much. — Ralph Waldo Emerson",
    "It is not the man who has too little, but the man who craves more, that is poor. — Seneca",
    "Wealth consists not in having great possessions, but in having few wants. — Epictetus",
    "Formal education will make you a living; self-education will make you a fortune. — Jim Rohn",
    "It’s not about having lots of money. It’s about knowing how to manage it. — Anonymous",
    "Do not save what is left after spending, but spend what is left after saving. — Warren Buffett",
    "The lack of money is the root of all evil. — Mark Twain",
    "Money can’t buy happiness, but it will certainly get you a better class of memories. — Ronald Reagan",
    "Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful. — Albert Schweitzer",
    "Time is money. — Benjamin Franklin",
    "A penny saved is a penny earned. — Benjamin Franklin",
    "You must gain control over your money or the lack of it will forever control you. — Dave Ramsey",
    "Rich people have small TVs and big libraries, and poor people have small libraries and big TVs. — Zig Ziglar",
    "If you don’t find a way to make money while you sleep, you will work until you die. — Warren Buffett",
    "Money is a terrible master but an excellent servant. — P.T. Barnum"
]

# to run the server
# fastapi dev .\main.py

@app.get("/")
def read_root():
    return {
        "message": "Hello World, Go to /side_hustles or /money_quotes to get a random side hustle or money quote"
    }

# http://127.0.0.1:8000/side_hustles?apikey=1234
@app.get("/side_hustles")
def get_side_hustles(apikey):
    """Return a Random Side Hustle"""
    if apikey != "1234":
        return{"error" :"invalid key" }
    return {"side_hustles": random.choice(side_hustles)}


# http://127.0.0.1:8000/money_quotes?apikey=1234
@app.get("/money_quotes")
def get_money_quotes(apikey):
    """Return a Random money quotes"""
    if apikey != "1234":
        return{"error" :"invalid key" }
    return {"money_quotes": random.choice(money_quotes)}
