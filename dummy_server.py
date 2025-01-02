from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os

app = FastAPI()

# Static responses for testing
DUMMY_USER = {"username": "testuser", "email": "testuser@example.com"}
DUMMY_CHAT_HISTORY = [
    {"chat_id": "123e4567-e89b-12d3-a456-426614174000", "chat_name": "Health Chat"},
    {"chat_id": "123e4567-e89b-12d3-a456-426614174001", "chat_name": "Fitness Chat"},
]
DUMMY_CONVERSATION = {
    "messages": [
        {"role": "user", "text": "Hello AI"},
        {"role": "bot", "text": "Hello! How can I assist you today?"},
    ]
}


# Models
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class ChatCreateRequest(BaseModel):
    chat_name: str
    conversation: dict


class ChatUpdateRequest(BaseModel):
    chat_id: str
    chat_name: str


class ChatDeleteRequest(BaseModel):
    chat_id: str


# User-related endpoints
@app.post("/user/register/")
async def register_user(request: RegisterRequest):
    return {"message": "User registered successfully", "user": request}


@app.post("/user/login/")
async def login_user(request: LoginRequest):
    if request.username == DUMMY_USER["username"] and request.password == "password123":
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")


@app.post("/user/logout/")
async def logout_user():
    return {"message": "Logout successful"}


# API endpoints
@app.post("/api/upload/")
async def upload_file(file_name: str, content: str):
    return {"message": "File uploaded successfully", "file_name": file_name}


@app.post("/api/prompt/")
async def prompt_response(prompt: str):
    return {"response": "This is a static response", "conversation": DUMMY_CONVERSATION}

@app.get("/api/chat-history/get/")
async def get_chat_history(chat_id: str):
    for chat in DUMMY_CHAT_HISTORY:
        if chat["chat_id"] == chat_id:
            return {"chat_id": chat_id, "chat_name": chat["chat_name"], "conversation": DUMMY_CONVERSATION}
    raise HTTPException(status_code=404, detail="Chat history not found")


@app.post("/api/chat-history/create/")
async def create_chat_history(request: ChatCreateRequest):
    return {"message": "Chat history created", "chat_name": request.chat_name}


@app.put("/api/chat-history/update/")
async def update_chat_history(request: ChatUpdateRequest):
    for chat in DUMMY_CHAT_HISTORY:
        if chat["chat_id"] == request.chat_id:
            chat["chat_name"] = request.chat_name
            return {"message": "Chat history updated", "chat_id": request.chat_id, "chat_name": request.chat_name}
    raise HTTPException(status_code=404, detail="Chat history not found")


@app.delete("/api/chat-history/delete/")
async def delete_chat_history(request: ChatDeleteRequest):
    for chat in DUMMY_CHAT_HISTORY:
        if chat["chat_id"] == request.chat_id:
            DUMMY_CHAT_HISTORY.remove(chat)
            return {"message": "Chat history deleted", "chat_id": request.chat_id}
    raise HTTPException(status_code=404, detail="Chat history not found")


@app.get("/api/chat-history/list/")
async def list_chat_ids_and_names():
    return [{"chat_id": chat["chat_id"], "chat_name": chat["chat_name"]} for chat in DUMMY_CHAT_HISTORY]


# Automatically start the server when the script is run
if __name__ == "__main__":
    import os
    import sys

    # Launch the FastAPI server using uvicorn
    try:
        print("Starting FastAPI server...")
        os.system(f"{sys.executable} -m uvicorn dummy_server:app --host 0.0.0.0 --port 8000 --reload")
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
