import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from .database import chat_collection

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env file")

# Initialize LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="openai/gpt-oss-20b"
)


def get_system_prompt(mode: str):
    if mode == "hr":
        return "You are an HR interviewer. Ask behavioral questions and give feedback."
    elif mode == "mock":
        return "You are a strict technical interviewer. Ask one question at a time and evaluate answers."
    else:
        return "You are a DSA expert. Answer clearly and concisely."


def get_history(user_id: str):
    chats = chat_collection.find({"user_id": user_id}).sort("timestamp", 1)
    history = []

    for chat in chats:
        history.append((chat["role"], chat["message"]))

    return history


def generate_response(user_id: str, question: str, mode: str):
    system_prompt = get_system_prompt(mode)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{history}"),
        ("human", "{question}")
    ])

    chain = prompt | llm

    history = get_history(user_id)

    response = chain.invoke({
        "history": history,
        "question": question
    })

    # Store user message
    chat_collection.insert_one({
        "user_id": user_id,
        "role": "human",
        "message": question,
        "timestamp": datetime.utcnow()
    })

    # Store assistant message
    chat_collection.insert_one({
        "user_id": user_id,
        "role": "assistant",
        "message": response.content,
        "timestamp": datetime.utcnow()
    })

    return response.content