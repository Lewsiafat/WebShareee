# Static Web Hosting Service

A simple and easy-to-use web service that allows users to upload static web pages and generate short URLs for sharing. This service provides a modern interface, supporting file uploads, code pasting, and comprehensive management functions.

## ✨ Features

- **Web Page Upload**: Supports HTML file uploads and direct pasting of source code.
- **Markdown Support**: Supports uploading Markdown files (.md) or pasting source code, which will be automatically converted and rendered as HTML pages.
- **Resource Files**: Supports associating static resources like images and PDFs with pages.
- **URL Generation**: Automatically generates unique short URLs for each page.
- **History Management**: Provides a dashboard to manage, view, and delete uploaded pages.
- **Secure Login**: Protects upload and management functions via an administrator account.
- **Account Management**: Provides a dedicated account settings page, allowing logged-in users to update their username and password at any time, ensuring account security.

## 🏗️ System Architecture

This project adopts a front-end and back-end separation architecture. The front-end is a Single Page Application (SPA) that communicates directly with the back-end API.

```
+-----------------+      +-------------------+
|   User Browser  | <--> |   FastAPI Backend |
+-----------------+      | (Uvicorn)         |
        |              +-------------------+
        |                      |
        | (API)                | (SQLite)
        v                      v
+-----------------+      +-------------------+
|   Vue.js Frontend|      |   Database        |
+-----------------+      +-------------------+
```

- **Frontend**: Built with Vue.js 3 and Vite, providing a responsive Single Page Application (SPA).
- **Backend**: Uses Python's FastAPI framework, responsible for handling API requests, user authentication, file uploads, and database interactions.
- **Database**: Uses SQLite as a lightweight database to store page information and user data.

## 🛠️ Technical Stack

### Frontend
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **UI Framework**: Element Plus
- **State Management**: Pinia
- **Routing**: Vue Router
- **HTTP Client**: Axios
- **Styling**: SCSS

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: SQLite
- **Package Manager**: uv
- **File Handling**: aiofiles, python-multipart

## 🚀 Installation and Setup

Please follow the steps below to set up your development environment:

### 1. Environment Preparation

Please ensure your system has the following software installed:
- [Node.js](https://nodejs.org/) (v18.0 or higher)
- [Python](https://www.python.org/) (v3.11 or higher)
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### 2. Backend Setup

```bash
# 1. Navigate to the backend directory
cd web-hosting-service/backend

# 2. Create a virtual environment using uv
uv venv

# 3. Activate the virtual environment
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# 4. Install Python dependencies
uv sync
```

### 3. Frontend Setup

```bash
# 1. Navigate to the frontend directory
cd web-hosting-service/frontend

# 2. Install Node.js dependencies
npm install
```

### 4. Start Development Server

This project provides a convenient startup script that can simultaneously launch both front-end and back-end development servers.

```bash
# Execute from the project root directory web-hosting-service/
./scripts/start.sh
```

- **Frontend** will run on `http://localhost:8080`
- **Backend** will run on `http://localhost:8700`

## ⚙️ Configuration

This project uses environment variables for backend configuration.

### Administrator Account

Upon the first startup of the system, a default administrator account will be created. You can configure it via the following environment variables:

- `DEFAULT_ADMIN_USERNAME`: Sets the default administrator username (default: `admin`)
- `DEFAULT_ADMIN_PASSWORD`: Sets the default administrator password (default: `adminpassword`)

**Important**: In a production environment, please ensure to set a strong password.

## 📝 Changelog

For detailed update records, please refer to [RELEASE_NOTES.md](RELEASE_NOTES.md).
