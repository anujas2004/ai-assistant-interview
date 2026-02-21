from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .models import ChatRequest, ChatResponse
from .chat_service import generate_response

app = FastAPI(title="AI Interview Assistant")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates folder (HTML)
templates = Jinja2Templates(directory="app/templates")


# -------------------------
# Home Route (Frontend UI)
# -------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# -------------------------
# Chat API Route
# -------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response_text = generate_response(
        user_id=request.user_id,
        question=request.question,
        mode=request.mode
    )
    return ChatResponse(response=response_text)