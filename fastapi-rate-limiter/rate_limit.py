# ============================================
# Rate Limiting API — Beginner Friendly Example
# ============================================

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# --- STEP 1: Create the rate limiter ---
# get_remote_address = identifies each user by their IP address
# default_limits = every user gets max 10 requests per minute (globally)
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

# --- STEP 2: Create the FastAPI app ---
app = FastAPI(
    title="Rate Limiting Demo",
    description="A beginner-friendly API to learn rate limiting",
)

# Attach the limiter to our app so it can track requests
app.state.limiter = limiter

# --- STEP 3: Handle what happens when someone exceeds the limit ---
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too Many Requests",
            "message": "You have exceeded the rate limit. Please slow down and try again later.",
        },
    )

# ============================================
# ROUTES (API Endpoints)
# ============================================


# ROUTE 1: Home — uses the global limit (10/minute)
@app.get("/")
async def home():
    return {
        "message": "Welcome to the Rate Limiting Demo API!",
        "tip": "Try hitting this endpoint many times quickly to see rate limiting in action.",
    }

# ROUTE 1: No limit — free for all
@app.get("/free")
@limiter.exempt
async def free_route():
    return {
        "message": "This route has NO rate limit. Hit it as many times as you want!",
    }

# ROUTE 2: Custom limit — only 3 requests per minute
@app.get("/limited")
@limiter.limit("3/minute")
async def limited_route(request: Request):
    return {
        "message": "This route only allows 3 requests per minute.",
        "status": "You are within the limit!",
    }

# ROUTE 3: Very strict — only 2 request every 1 hour
@app.get("/super-limited")
@limiter.limit("2/10 hours")
async def super_limited_route(request: Request):
    return {
        "message": "This route only allows 2 request every 10 hours.",
        "status": "You got through!",
    }