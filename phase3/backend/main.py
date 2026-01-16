from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from models import User, Conversation, Message
from db import engine, create_db_and_tables
from agent import run_agent
import os

app = FastAPI(title="Todo Chatbot API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
        "https://hackathon-todo-lac.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list


@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Todo Chatbot API - Phase III"}


@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(user_id: str, request: ChatRequest):
    """
    Stateless chat endpoint that persists conversation state to database.
    
    Flow:
    1. Auto-create user if doesn't exist
    2. Get or create conversation
    3. Store user message
    4. Fetch conversation history
    5. Build message array for agent
    6. Run agent with MCP tools
    7. Store assistant response
    8. Return response to client
    """
    
    with Session(engine) as session:
        # ✅ FIX: Auto-create user if doesn't exist
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            now = datetime.utcnow()
            user = User(
                id=user_id,
                email=f"{user_id}@demo.local",
                name=user_id.replace("-", " ").title(),
                password="demo-password-hash",  # ✅ Required by database
                created_at=now,
                updated_at=now  # ✅ Required by database
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        
        # Get or create conversation
        if request.conversation_id:
            conversation = session.exec(
                select(Conversation)
                .where(Conversation.id == request.conversation_id)
                .where(Conversation.user_id == user_id)
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        
        # Fetch conversation history
        statement = select(Message).where(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at)
        history = session.exec(statement).all()
        
        # Build message array for agent
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in history
        ]
        
        # Add new user message
        messages.append({"role": "user", "content": request.message})
        
        # Store user message in database
        user_message = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=request.message
        )
        session.add(user_message)
        session.commit()
        
        # Run agent
        try:
            result = await run_agent(user_id, messages)
            
            # Store assistant response in database
            assistant_message = Message(
                conversation_id=conversation.id,
                user_id=user_id,
                role="assistant",
                content=result["response"]
            )
            session.add(assistant_message)
            session.commit()
            
            # Return response
            return ChatResponse(
                conversation_id=conversation.id,
                response=result["response"],
                tool_calls=result["tool_calls"]
            )
        except Exception as e:
            session.rollback()
            print(f"❌ Error in agent: {e}")  # Debug log
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/{user_id}/conversations")
def list_conversations(user_id: str):
    """List all conversations for a user."""
    with Session(engine) as session:
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc())
        conversations = session.exec(statement).all()
        return {"conversations": conversations}


@app.get("/api/{user_id}/conversations/{conversation_id}")
def get_conversation(user_id: str, conversation_id: int):
    """Get conversation with full message history."""
    with Session(engine) as session:
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at)
        messages = session.exec(statement).all()
        
        return {
            "conversation": conversation,
            "messages": messages
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
