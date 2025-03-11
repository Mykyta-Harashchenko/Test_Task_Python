import os
from contextlib import asynccontextmanager
import re
import logging
import requests
import openai
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from sqlalchemy.ext.asyncio import AsyncSession
from bs4 import BeautifulSoup
from fastapi.responses import FileResponse

from Project.src.database.db import get_db
from Project.src.entity.models import User, Message
from Project.src.routes.promtps import extract_url, fetch_page_content
from Project.src.schemas.chat import MessageScheme
from Project.src.routes.auth import router as auth_router
from fastapi_limiter.depends import RateLimiter
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text, select
from Project.src.conf.config import config
from Project.src.services.dependencies import get_current_user


logging.basicConfig(level=logging.DEBUG)
app = FastAPI(title="Test Task")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.mount("/static", StaticFiles(directory="Project/static"), name="static")

@app.get("/api/healthchecker", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
async def serve_index():
    return FileResponse("Project/static/index.html")

@app.post("/chat/")
async def chat(
    request: MessageScheme,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    messages = [{"role": "user", "content": request.message}]
    url = extract_url(request.message)
    if url:
        page_content = fetch_page_content(url)
        messages.append({"role": "system", "content": f"Вот текст страницы {url}: {page_content}"})
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        answer_text = response.choices[0].message.content
        new_message = Message(
            request=request.message,
            answer=answer_text,
            sender_id=current_user.id,
        )
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)
        return {"response": answer_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history")
async def get_chat_history(
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Message)
            .where(Message.sender_id == current_user.id)
            .order_by(Message.id)
        )
        messages = result.scalars().all()
        history = [
            {
                "request": msg.request,
                "answer": msg.answer,
            }
            for msg in messages
        ]
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

