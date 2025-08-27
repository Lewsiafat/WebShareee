# 靜態網頁託管服務 (Static Web Hosting Service)

一個簡單易用的網站服務，讓使用者能夠上傳靜態網頁並產生短網址進行分享。本服務提供了一個現代化的介面，支援檔案上傳、程式碼貼上，以及完整的管理功能。

## ✨ 功能特色 (Features)

- **網頁上傳**: 支援 HTML 檔案上傳與直接貼上原始碼。
- **Markdown 支援**: 支援上傳 Markdown 檔案 (.md) 或貼上原始碼，並自動轉換為 HTML 頁面。
- **資源檔案**: 支援圖片、PDF 等靜態資源與頁面關聯。
- **URL 生成**: 自動為每個頁面生成獨特的短網址。
- **歷史管理**: 提供儀表板來管理、檢視及刪除已上傳的頁面。
- **安全登入**: 透過管理員帳號保護上傳與管理功能。
- **帳號管理**: 提供獨立的帳號設定頁面，允許登入後的使用者隨時更新自己的使用者名稱和密碼，確保帳號安全。

## 🏗️ 系統架構 (System Architecture)

本專案採用前後端分離的架構。前端是一個單頁應用程式 (SPA)，直接與後端 API 進行通訊。

```
+-----------------+      +-------------------+
|   使用者 Browser | <--> |   FastAPI Backend |
+-----------------+      | (Uvicorn)         |
        |              +-------------------+
        |                      |
        | (API)                | (SQLite)
        v                      v
+-----------------+      +-------------------+
|   Vue.js Frontend|      |   Database        |
+-----------------+      +-------------------+
```

- **前端 (Frontend)**: 使用 Vue.js 3 搭配 Vite 建置，提供一個響應式的單頁應用程式 (SPA)。
- **後端 (Backend)**: 使用 Python 的 FastAPI 框架，負責處理 API 請求、使用者認證、檔案上傳和資料庫互動。
- **資料庫 (Database)**: 使用 SQLite 作為輕量級的資料庫，儲存頁面資訊和使用者資料。

## 🛠️ 技術背景 (Technical Stack)

### 前端 (Frontend)
- **框架**: Vue 3 (Composition API)
- **建構工具**: Vite
- **UI 框架**: Element Plus
- **狀態管理**: Pinia
- **路由**: Vue Router
- **HTTP 客戶端**: Axios
- **樣式**: SCSS

### 後端 (Backend)
- **語言**: Python 3.11+
- **框架**: FastAPI
- **伺服器**: Uvicorn
- **資料庫**: SQLite
- **套件管理**: uv
- **檔案處理**: aiofiles, python-multipart

## 🚀 安裝與啟動 (Installation and Setup)

請依照以下步驟設定開發環境：

### 1. 環境準備

請先確認您的系統已安裝以下軟體：
- [Node.js](https://nodejs.org/) (v18.0 或以上)
- [Python](https://www.python.org/) (v3.11 或以上)
- [uv](https://github.com/astral-sh/uv) (Python 套件管理器)

### 2. 後端設定 (Backend)

```bash
# 1. 進入後端目錄
cd web-hosting-service/backend

# 2. 使用 uv 建立虛擬環境
uv venv

# 3. 啟用虛擬環境
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# 4. 安裝 Python 依賴套件
uv sync
```

### 3. 前端設定 (Frontend)

```bash
# 1. 進入前端目錄
cd web-hosting-service/frontend

# 2. 安裝 Node.js 依賴套件
npm install
```

### 4. 啟動開發伺服器

本專案提供一個方便的啟動腳本，可以同時啟動前後端開發伺服器。

```bash
# 於專案根目錄 web-hosting-service/ 執行
./scripts/start.sh
```

- **前端** 將會運行在 `http://localhost:8080`
- **後端** 將會運行在 `http://localhost:8700`

## ⚙️ 設定與組態 (Configuration)

本專案使用環境變數進行後端設定。

### 管理員帳號

在系統首次啟動時，會建立一組預設的管理員帳號。您可以透過以下環境變數進行設定：

- `DEFAULT_ADMIN_USERNAME`: 設定預設管理員的使用者名稱 (預設值: `admin`)
- `DEFAULT_ADMIN_PASSWORD`: 設定預設管理員的密碼 (預設值: `adminpassword`)

**重要**: 在生產環境中，請務必設定一個高強度的密碼。

## 📝 版本歷史 (Changelog)

詳細的更新紀錄請參考 [RELEASE_NOTES.md](RELEASE_NOTES.md)。