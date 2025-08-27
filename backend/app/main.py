import os
import shutil
import secrets
import string
import markdown
import logging
from typing import Optional, List
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from passlib.context import CryptContext

from . import database, schemas
from .database import engine, SessionLocal, create_db_and_tables, Page, Asset, User

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Static Web Hosting Service Backend",
    description="API for uploading and serving static web pages.",
    version="0.1.0"
)

# --- CORS Middleware ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Setup ---
@app.on_event("startup")
def on_startup():
    logger.info("Application startup: Creating database and tables...")
    create_db_and_tables()
    db = SessionLocal()
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        if db.query(User).count() == 0:
            logger.info("No admin user found. Creating default admin user.")
            default_username = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
            default_password = os.getenv("DEFAULT_ADMIN_PASSWORD", "adminpassword")
            hashed_password = pwd_context.hash(default_password)
            default_user = User(username=default_username, hashed_password=hashed_password)
            db.add(default_user)
            db.commit()
            logger.info(f"Default admin user '{default_username}' created.")
        else:
            logger.info("Admin user already exists. Skipping default creation.")
    except Exception as e:
        logger.error(f"Error during startup user creation: {e}", exc_info=True)
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Security Setup (HTTP Basic Auth) ---
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_username(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    logger.debug(f"Attempting to authenticate user: {credentials.username}")
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        logger.warning(f"Authentication failed for user: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    logger.info(f"User authenticated successfully: {user.username}")
    return user.username

# --- File Storage Configuration ---
CURRENT_FILE_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = CURRENT_FILE_DIR.parent.parent.parent.resolve()
UPLOAD_DIR = PROJECT_ROOT / "backend" / "uploads"
PAGES_DIR = UPLOAD_DIR / "pages"
PAGES_DIR.mkdir(parents=True, exist_ok=True)
logger.info(f"Upload directory configured at: {PAGES_DIR}")

# --- Helper Functions ---
def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    confusing_chars = "0Ol1"
    valid_chars = "".join(c for c in chars if c not in confusing_chars)
    return ''.join(secrets.choice(valid_chars) for _ in range(length))

def get_unique_page_id(db: Session):
    while True:
        page_id = generate_short_id()
        if not db.query(Page).filter(Page.id == page_id).first():
            return page_id

# --- API Endpoints ---

# Authentication
@app.post("/api/auth/login", summary="Admin Login")
async def login(username: str = Depends(get_current_username)):
    logger.info(f"User '{username}' logged in successfully.")
    return {"message": f"Welcome, {username}! Login successful."}

# Upload HTML or Markdown File
@app.post("/api/upload/html", summary="Upload HTML or Markdown File")
async def upload_html_file(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
):
    logger.info(f"Received file upload request: '{file.filename}' by user '{current_user}'")
    filename = file.filename
    if not (filename.endswith(".html") or filename.endswith(".md") or filename.endswith(".markdown")):
        logger.warning(f"Invalid file type uploaded: {filename}")
        raise HTTPException(status_code=400, detail="Only .html, .md, or .markdown files are allowed.")

    page_id = get_unique_page_id(db)
    page_dir = PAGES_DIR / page_id
    page_dir.mkdir(parents=True, exist_ok=True)
    html_file_path = page_dir / "index.html"

    try:
        content_bytes = await file.read()
        
        if filename.endswith(".md") or filename.endswith(".markdown"):
            logger.info(f"Converting Markdown file '{filename}' to HTML.")
            md_content = content_bytes.decode("utf-8")
            html_content = markdown.markdown(md_content)
            with open(html_file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
        else: # HTML file
            logger.info(f"Saving HTML file '{filename}'.")
            with open(html_file_path, "wb") as f:
                f.write(content_bytes)

    except Exception as e:
        logger.error(f"Error processing file '{filename}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing file.")
    finally:
        await file.close()

    db_page = Page(id=page_id, title=title if title else filename, file_path=str(html_file_path), html_content=None)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    logger.info(f"Successfully created page '{page_id}' from file '{filename}'.")
    return {"id": db_page.id, "title": db_page.title, "url": f"/p/{db_page.id}", "created_at": db_page.created_at}

# Upload HTML Code
@app.post("/api/upload/code", summary="Upload HTML Code")
async def upload_html_code(
    payload: schemas.HtmlCodeUpload,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
):
    logger.info(f"Received HTML code upload request by user '{current_user}'")
    page_id = get_unique_page_id(db)
    page_dir = PAGES_DIR / page_id
    page_dir.mkdir(parents=True, exist_ok=True)
    html_file_path = page_dir / "index.html"

    try:
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(payload.html_content)
    except Exception as e:
        logger.error(f"Failed to write HTML content for new page: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to write HTML content: {e}")

    db_page = Page(id=page_id, title=payload.title if payload.title else "Untitled Page", file_path=str(html_file_path), html_content=payload.html_content)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    logger.info(f"Successfully created page '{page_id}' from HTML code.")
    return {"id": db_page.id, "title": db_page.title, "url": f"/p/{db_page.id}", "created_at": db_page.created_at}

# Upload Markdown Code
@app.post("/api/upload/markdown", summary="Upload Markdown Code")
async def upload_markdown_code(
    payload: schemas.MarkdownCodeUpload,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
):
    logger.info(f"Received Markdown code upload request by user '{current_user}'")
    page_id = get_unique_page_id(db)
    page_dir = PAGES_DIR / page_id
    page_dir.mkdir(parents=True, exist_ok=True)
    html_file_path = page_dir / "index.html"

    html_content = markdown.markdown(payload.markdown_content)

    try:
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
    except Exception as e:
        logger.error(f"Failed to write converted HTML content for new page: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to write HTML content: {e}")

    db_page = Page(id=page_id, title=payload.title if payload.title else "Untitled Page", file_path=str(html_file_path), html_content=payload.markdown_content)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    logger.info(f"Successfully created page '{page_id}' from Markdown code.")
    return {"id": db_page.id, "title": db_page.title, "url": f"/p/{db_page.id}", "created_at": db_page.created_at}

# ... (rest of the endpoints with logging added) ...

# Serve Page and Increment View Count
@app.get("/p/{page_id}", summary="Serve Page and Increment View Count", response_class=HTMLResponse)
async def serve_page(page_id: str, db: Session = Depends(get_db)):
    logger.debug(f"Request received for page: {page_id}")
    page = db.query(Page).filter(Page.id == page_id, Page.is_active == True).first()
    if not page:
        logger.warning(f"Page not found or inactive: {page_id}")
        raise HTTPException(status_code=404, detail="Page not found or is inactive.")

    page.view_count += 1
    db.commit()
    logger.info(f"Serving page '{page_id}'. New view count: {page.view_count}")

    html_file_path = Path(page.file_path)
    if not html_file_path.exists():
        logger.error(f"File not found for page '{page_id}' at path: {html_file_path}")
        raise HTTPException(status_code=404, detail="HTML content not found for this page.")

    with open(html_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content)
