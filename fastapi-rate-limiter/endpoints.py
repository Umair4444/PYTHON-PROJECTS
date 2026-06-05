# Singup - Login & JWT Authentication with FastAPI
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
import jwt
from datetime import datetime, timedelta, timezone

# Secret Key for the Server
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # In production, use environment variable!
ALGORITHM = "HS256" # JWT Algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token Expiry Time in Minutes

app = FastAPI()
password_hasher = PasswordHash((BcryptHasher(),))

# ---- OAuth2 Scheme ----
# This will be used to extract the token from the Authorization header in protected routes
# tokenUrl is the endpoint where the client will send the username and password to get the token (in this case, it's our /sign-in endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="sign-in")

# User Model
class UserCreate(BaseModel):
    username: str
    password: str

# fake_db
fake_db = []
# token_blacklist stores tokens that have been logged out
token_blacklist = set()

###### Utility Functions ######

# Hash the password using bcrypt
def hash_password(plain_password: str) -> str:
    return password_hasher.hash(plain_password)

# Verify the password against the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)

# ---- JWT Functions ----
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> dict:
    if token in token_blacklist:
        raise HTTPException(status_code=401, detail="Token has been logged out!")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired!")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token!")

# Step 1. Sign Up / Registration Endpoint
@app.post("/register")
async def register(user: UserCreate):
    for existing_user in fake_db:
        if existing_user['username'] == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user.password)
    fake_db.append({"username": user.username, "password": hashed_password})
    return {"message": f"User {user.username} registered successfully"}

# Step 2. Login / SignIn Endpoint
@app.post("/sign-in")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Step 1: Find user
    user = None
    for u in fake_db:
        if u["username"] == form_data.username:
            user = u
            break
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username!")
    
    # Step 2: Verify password
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password!")
    
    # Step 3: Create JWT token
    access_token = create_access_token(data={"sub": user["username"]})
    
    # on successful login, return the access token and it will always be same for the same user until the token expires and if user logs in again (even with the same credentials), a new token will be generated
    return {"message": f"User {user['username']} logged in successfully!", "access_token": access_token, "token_type": "bearer"}

# Step 3. Logout Endpoint
@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Verify token is valid before blacklisting
    verify_token(token)
    token_blacklist.add(token)
    return {"message": "Successfully logged out"}

# Step 4. Protected Route
@app.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    username = payload.get("sub")
    return {"username": username, "message": f"Hello {username}! You are authenticated!"}

# For testing purposes only: Get all users with password (not recommended in production)
@app.get("/all-users")
async def get_all_users():
    return {"users": [user["username"] for user in fake_db], "passwords": [user["password"] for user in fake_db]}