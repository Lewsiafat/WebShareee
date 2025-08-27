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

# Upload Asset
@app.post("/api/upload/asset/{page_id}", summary="Upload Asset for a Page")
async def upload_asset(
    page_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
):
    logger.info(f"User '{current_user}' uploading asset '{file.filename}' for page '{page_id}'")
    page = db.query(Page).filter(Page.id == page_id, Page.is_active == True).first()
    if not page:
        logger.warning(f"Page not found: {page_id}")
        raise HTTPException(status_code=404, detail="Page not found.")

    asset_dir = PAGES_DIR / page_id / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    asset_file_path = asset_dir / file.filename

    try:
        with open(asset_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"Failed to save asset '{file.filename}' for page '{page_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to save asset.")
    finally:
        file.file.close()

    db_asset = Asset(
        page_id=page_id,
        file_name=file.filename,
        file_type=file.content_type,
        file_path=str(asset_file_path)
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    logger.info(f"Asset '{file.filename}' uploaded successfully for page '{page_id}'.")
    return {"message": f"Asset '{file.filename}' uploaded successfully for page '{page_id}'."}

# Get All Pages
@app.get("/api/pages", response_model=List[schemas.PageResponse], summary="Get All Pages")
async def get_all_pages(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
):
    logger.info(f"User '{current_user}' fetching all pages.")
    pages = db.query(Page).filter(Page.is_active == True).all()
    response_pages = []
    for page in pages:
        response_pages.append(schemas.PageResponse(
            id=page.id,
            title=page.title,
            url=f"/p/{page.id}",
            created_at=page.created_at,
            view_count=page.view_count,
            is_active=page.is_active
        ))
    return response_pages

# Get Page Details
@app.get("/api/pages/{page_id}", response_model=schemas.PageResponse, summary="Get Page Details")
async def get_page_details(
    page_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
):
    logger.info(f"User '{current_user}' fetching details for page '{page_id}'.")
    page = db.query(Page).filter(Page.id == page_id, Page.is_active == True).first()
    if not page:
        logger.warning(f"Page not found: {page_id}")
        raise HTTPException(status_code=404, detail="Page not found.")
    
    return schemas.PageResponse(
        id=page.id,
        title=page.title,
        url=f"/p/{page.id}",
        created_at=page.created_at,
        view_count=page.view_count,
        is_active=page.is_active
    )

# Delete Page (Soft Delete)
@app.delete("/api/pages/{page_id}", summary="Delete Page (Soft Delete)")
async def delete_page(
    page_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
):
    logger.info(f"User '{current_user}' deleting page '{page_id}'.")
    page = db.query(Page).filter(Page.id == page_id, Page.is_active == True).first()
    if not page:
        logger.warning(f"Page not found for deletion: {page_id}")
        raise HTTPException(status_code=404, detail="Page not found.")

    page.is_active = False
    db.commit()
    logger.info(f"Page '{page_id}' soft-deleted successfully.")
    return {"message": f"Page '{page_id}' soft-deleted successfully."}

# Update Page Details
@app.put("/api/pages/{page_id}", response_model=schemas.PageResponse, summary="Update Page Details")
async def update_page(
    page_id: str,
    page_update: schemas.PageUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_username)
):
    logger.info(f"User '{current_user}' updating page '{page_id}'.")
    page = db.query(Page).filter(Page.id == page_id, Page.is_active == True).first()
    if not page:
        logger.warning(f"Page not found for update: {page_id}")
        raise HTTPException(status_code=404, detail="Page not found.")

    if page_update.title is not None:
        page.title = page_update.title

    db.commit()
    db.refresh(page)
    logger.info(f"Page '{page_id}' updated successfully.")
    return schemas.PageResponse(
        id=page.id,
        title=page.title,
        url=f"/p/{page.id}",
        created_at=page.created_at,
        view_count=page.view_count,
        is_active=page.is_active
    )

# Change Admin Password
@app.put("/api/admin/password", summary="Change Admin Password")
async def change_admin_password(
    password_change: schemas.PasswordChange,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_username)
):
    logger.info(f"User '{current_user_username}' attempting to change password.")
    user = db.query(User).filter(User.username == current_user_username).first()
    if not user:
        logger.error(f"User not found: {current_user_username}")
        raise HTTPException(status_code=404, detail="User not found.")

    if not verify_password(password_change.old_password, user.hashed_password):
        logger.warning(f"Incorrect password for user '{current_user_username}' during password change")
        raise HTTPException(status_code=400, detail="Incorrect old password.")

    user.hashed_password = pwd_context.hash(password_change.new_password)
    db.commit()
    logger.info(f"Password for user '{current_user_username}' changed successfully.")
    return {"message": "Password changed successfully."}


# Change Admin Username
@app.put("/api/admin/username", summary="Change Admin Username")
async def change_admin_username(
    username_change: schemas.UsernameChange,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_username)
):
    logger.info(f"User '{current_user_username}' attempting to change username to '{username_change.new_username}'")
    user = db.query(User).filter(User.username == current_user_username).first()
    if not user:
        logger.error(f"User not found: {current_user_username}")
        raise HTTPException(status_code=404, detail="User not found.")

    if not verify_password(username_change.password, user.hashed_password):
        logger.warning(f"Incorrect password for user '{current_user_username}' during username change")
        raise HTTPException(status_code=400, detail="Incorrect password.")

    if db.query(User).filter(User.username == username_change.new_username).first():
        logger.warning(f"Username '{username_change.new_username}' is already taken.")
        raise HTTPException(status_code=400, detail="Username is already taken.")

    user.username = username_change.new_username
    db.commit()
    logger.info(f"Username for user '{current_user_username}' successfully changed to '{username_change.new_username}'")
    return {"message": "Username changed successfully."}


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
