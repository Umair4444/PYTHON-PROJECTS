# 📚 Quote Share – Full Stack Web App

This is a simple full-stack project that fetches and displays random quotes using:

- 🧠 **Backend**: Python with FastAPI, served using `uvicorn`
- 💻 **Frontend**: Next.js with TypeScript

---

## ✨ Features

- Fetch a random inspirational quote with a single click
- Built using modern, lightweight tools
- Demonstrates frontend-backend communication with CORS
- Great for learning full-stack basics

---

## 📁 Project Structure

quote-share/
├── backend/ # Python FastAPI backend
│     └── main.py
├── frontend/ # Next.js frontend
│     └── app/page.tsx
├── readme.md


1. Backend Setup

Requirements:
Python 3.8+

uv venv
activate venv 
uv init backend

Install Dependencies

cd backend
uv add fastapi uvicorn

Run the Server
uvicorn main:app --reload --port 8000

The backend will be running at:
📡 http://localhost:8000/quote


2. frontend

npx create-next-app@latest frontend 
cd frontend
npm install axios

Start the Dev Server
npm run dev

The frontend will be available at:
🌐 http://localhost:3000
