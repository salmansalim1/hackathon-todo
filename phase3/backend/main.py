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

app = FastAPI(title="Todo Chatbot API - Phase III")

# CORS configuration - Allow Vercel deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
        "https://*.vercel.app",
        "https://hackathon-todo-chatbot.vercel.app/",  # Allow all Vercel preview deployments
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
    print("🚀 Starting Todo Chatbot API - Phase III")
    print("📊 Initializing database...")
    create_db_and_tables()
    print("✅ Database initialized successfully")


@app.get("/")
def root():
    return {
        "message": "Todo Chatbot API - Phase III",
        "status": "running",
        "endpoints": {
            "chat": "/api/{user_id}/chat",
            "conversations": "/api/{user_id}/conversations",
            "health": "/health"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "Todo Chatbot API",
        "phase": "III",
        "database": "connected"
    }


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
    print(f"📨 Received chat request from user: {user_id}")
    print(f"💬 Message: {request.message}")
    
    try:
        with Session(engine) as session:
            # Auto-create user if doesn't exist
            user = session.exec(select(User).where(User.id == user_id)).first()
            if not user:
                print(f"👤 Creating new user: {user_id}")
                now = datetime.utcnow()
                user = User(
                    id=user_id,
                    email=f"{user_id}@demo.local",
                    name=user_id.replace("-", " ").title(),
                    password="demo-password-hash",
                    created_at=now,
                    updated_at=now
                )
                session.add(user)
                session.commit()
                session.refresh(user)
                print(f"✅ User created: {user_id}")

            # Get or create conversation
            if request.conversation_id:
                print(f"🔍 Looking for conversation ID: {request.conversation_id}")
                conversation = session.exec(
                    select(Conversation)
                    .where(Conversation.id == request.conversation_id)
                    .where(Conversation.user_id == user_id)
                ).first()
                if not conversation:
                    raise HTTPException(status_code=404, detail="Conversation not found")
                print(f"✅ Found existing conversation: {conversation.id}")
            else:
                # Create new conversation
                print("🆕 Creating new conversation")
                conversation = Conversation(user_id=user_id)
                session.add(conversation)
                session.commit()
                session.refresh(conversation)
                print(f"✅ New conversation created: {conversation.id}")

            # Fetch conversation history
            statement = select(Message).where(
                Message.conversation_id == conversation.id
            ).order_by(Message.created_at)
            history = session.exec(statement).all()
            print(f"📜 Loaded {len(history)} messages from history")

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
            print("💾 User message stored in database")

            # Run agent
            print("🤖 Running AI agent...")
            result = await run_agent(user_id, messages)
            print(f"✅ Agent response: {result['response'][:100]}...")
            print(f"🔧 Tool calls: {len(result['tool_calls'])}")

            # Store assistant response in database
            assistant_message = Message(
                conversation_id=conversation.id,
                user_id=user_id,
                role="assistant",
                content=result["response"]
            )
            session.add(assistant_message)
            session.commit()
            print("💾 Assistant response stored in database")

            # Return response
            response = ChatResponse(
                conversation_id=conversation.id,
                response=result["response"],
                tool_calls=result["tool_calls"]
            )
            print(f"✅ Sending response for conversation {conversation.id}")
            return response

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/api/{user_id}/conversations")
def list_conversations(user_id: str):
    """List all conversations for a user."""
    print(f"📋 Listing conversations for user: {user_id}")
    try:
        with Session(engine) as session:
            statement = select(Conversation).where(
                Conversation.user_id == user_id
            ).order_by(Conversation.updated_at.desc())
            conversations = session.exec(statement).all()
            print(f"✅ Found {len(conversations)} conversations")
            return {"conversations": conversations}
    except Exception as e:
        print(f"❌ Error listing conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/{user_id}/conversations/{conversation_id}")
def get_conversation(user_id: str, conversation_id: int):
    """Get conversation with full message history."""
    print(f"🔍 Getting conversation {conversation_id} for user {user_id}")
    try:
        with Session(engine) as session:
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(status_code=404, detail="Conversation not found")

            statement = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.created_at)
            messages = session.exec(statement).all()
            print(f"✅ Found conversation with {len(messages)} messages")

            return {
                "conversation": conversation,
                "messages": messages
            }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
