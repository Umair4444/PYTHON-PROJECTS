from fastapi import FastAPI
import random

app = FastAPI()

fake_info = {
    
  "fictional_bio":[
    "Born in a remote Himalayan village, raised by monks and scientists.",
    "Built a solar-powered drone at the age of 10.",
    "Fluent in 8 languages, including Swahili and Japanese Sign Language.",
    "Holds triple PhDs in Quantum Physics, Philosophy, and Artificial Intelligence.",
    "Was featured in Forbes “30 Under 30” at age 17.",
    "Designed a microprocessor now used in NASA rovers.",
    "Co-authored a book with Elon Musk.",
    "Interned at CERN at 15 and discovered an anomaly in the Higgs boson field.",
    "Runs a foundation for educating underprivileged AI prodigies.",
    "Certified deep-sea diver and part-time marine archaeologist.",
    "Built an AI to compose classical symphonies indistinguishable from Mozart’s.",
    "Interviewed live by Oprah and impressed her with a 6-line haiku in Swahili.",
    "Was a chess grandmaster at 13.",
    "Speaks in riddles when coding in Python for fun.",
    "Climbed Mount Kilimanjaro barefoot for a charity event.",
    "Consulted by the UN on climate change strategy.",
    "Hosted a TED Talk that went viral with 500M+ views.",
    "Has a photographic memory and can recite all digits of Pi (up to 10,000).",
    "Built a holographic AI twin for real-time global speeches.",
    "Worked with Marvel Studios to design CGI for Iron Man’s suit.",
    "Wrote and directed an award-winning indie sci-fi film.",
    "Discovered a new species of orchid named after them.",
    "Has an asteroid named in their honor.",
    "Once solved a Rubik’s cube mid-skydive.",
    "Designed a cryptocurrency system used in over 50 countries.",
    "Was invited to Area 51 to consult on “classified” projects.",
    "Can play 14 musical instruments, 7 of which are rare and ancient.",
    "Founded a green-tech startup worth $1.2B.",
    "Wrote an AI model to mimic Shakespearean writing and passed the Turing test.",
    "Created a VR meditation experience used in NASA’s space missions.",
    "Rescued a stranded whale using drone tech.",
    "Started a YouTube channel with 200M subscribers in a year.",
    "Has an honorary knighthood from the UK for digital innovation.",
    "Composed background music for major Netflix shows.",
    "Designed a self-healing robotic skin.",
    "Delivered a keynote at Google I/O at age 19.",
    "Cracked a 50-year-old encrypted Soviet code for fun.",
    "Won a global poetry slam with a spoken word AI co-writer.",
    "Helped reverse-engineer dinosaur DNA (fictionally, of course).",
    "Mentored 100 young inventors globally via hologram tech.",
    "Runs a luxury vegan chocolate brand shipped worldwide.",
    "Discovered an ancient manuscript believed to be Leonardo da Vinci’s.",
    "Appeared on Time Magazine’s cover twice.",
    "Developed a mobile app that plants a tree with every download.",
    "Created the world’s first emotion-sensing wearable.",
    "Teaches mindfulness to Fortune 500 CEOs.",
    "Designed eco-friendly architecture in Antarctica.",
    "Led a successful Mars colonization simulation.",
    "Created a global language for interspecies communication.",
    "Starred in a reality show about genius coders.",
    "Defeated the world’s fastest AI in a logic game.",
    "Helped preserve 12 endangered cultures using VR.",
    "Designed an algorithm that predicts trends 3 years in advance.",
    "Flew a supersonic jet on their 21st birthday.",
    "Won “Best Dressed Innovator” at the Metaverse Gala.",
    "Raced solar cars across the Sahara for a documentary.",
    "Built a city in Minecraft that became a global virtual classroom.",
    "Serves as honorary president of the International Nerd Alliance.",
    "Wrote a romantic novel under a pseudonym that topped best-seller lists.",
    "Invented a biodegradable smartphone.",
    "Trains parrots to deliver micro USB drives.",
    "Pilots a drone show in Times Square every New Year.",
    "Discovered a technique to grow vegetables using sound waves.",
    "Built an underwater AI lab off the coast of Iceland.",
    "Featured on a special edition stamp in Japan.",
    "Conducts midnight radio shows on quantum humor.",
    "Created a mental health chatbot used by 10M+ teens.",
    "Developed a face recognition system that detects emotions.",
    "Won a global dance-off using robot choreography.",
    "Created the world’s smallest AI-powered camera.",
    "Authored a children’s book on blockchain.",
    "Flawlessly impersonated 10 historical figures at a U.N. gala.",
    "Designed a solar-powered smart shoe.",
    "Can juggle while solving math problems blindfolded.",
    "Built a treehouse that adjusts to weather via AI.",
    "Consults with world leaders on ethical AI.",
    "Once made friends with a wild cheetah while coding in the jungle.",
    "Ranks top 0.001% in global IQ simulations.",
    "Served as a part-time astronaut (yes, fictionally!).",
    "Translated the Epic of Gilgamesh into emoji.",
    "Created a language-learning game downloaded in 190+ countries.",
    "Wrote a machine learning algorithm that predicts plot twists.",
    "Started the “Hack For Humanity” global challenge.",
    "Was awarded “Most Likely to Time Travel” in high school.",
    "Designed an interactive museum powered by neural networks.",
    "Can code with both hands simultaneously on two keyboards.",
    "Hosts a secret society of global inventors.",
    "Can mimic 50+ accents perfectly.",
    "Invented a tea that improves memory recall.",
    "Conducted a symphony of robot musicians at Carnegie Hall.",
    "Launched a climate-change campaign backed by 100+ celebrities.",
    "Created a browser extension that blocks negativity.",
    "Built a pet robot that writes poems.",
    "Wrote a Python script to automate their entire smart home.",
    "Was once voted “Most Interesting Person on the Internet.”",
    "Rebuilt the Titanic in VR as a historical archive.",
    "Built a drone that can paint murals.",
    "Created an app that scans emotions through text.",
    "Dreams in code — literally.",
    "Plans to build the world’s first city powered entirely by thought."
]}

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
        "message": "Hello World, Go to /side_hustles or /money_quotes to get a random side hustle or money quote and /fakeinfo for the fake information about myself"
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

# 
@app.get("/fakeinfo")
def umair_fake_info():
    """Return Fake info"""
    return fake_info
