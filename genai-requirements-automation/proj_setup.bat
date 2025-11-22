@echo off
SET ROOT=genai-requirements-automation

REM Create root folder
mkdir %ROOT%

REM Backend structure
mkdir %ROOT%\backend
mkdir %ROOT%\backend\routers
mkdir %ROOT%\backend\core
mkdir %ROOT%\backend\data
mkdir %ROOT%\backend\data\spec
mkdir %ROOT%\backend\data\generated
mkdir %ROOT%\backend\data\embeddings
mkdir %ROOT%\backend\data\downloads

REM Create backend files
type nul > %ROOT%\backend\app.py
type nul > %ROOT%\backend\requirements.txt

type nul > %ROOT%\backend\routers\upload.py
type nul > %ROOT%\backend\routers\generate.py
type nul > %ROOT%\backend\routers\ado.py
type nul > %ROOT%\backend\routers\chatbot.py
type nul > %ROOT%\backend\routers\download.py

type nul > %ROOT%\backend\core\config.py
type nul > %ROOT%\backend\core\embeddings.py
type nul > %ROOT%\backend\core\rag_retriever.py
type nul > %ROOT%\backend\core\llm_engine.py
type nul > %ROOT%\backend\core\vectorstore.py
type nul > %ROOT%\backend\core\document_parser.py
type nul > %ROOT%\backend\core\file_generator.py

REM Frontend structure
mkdir %ROOT%\frontend
mkdir %ROOT%\frontend\src
mkdir %ROOT%\frontend\src\components
mkdir %ROOT%\frontend\src\services

REM Create frontend files
type nul > %ROOT%\frontend\src\App.jsx
type nul > %ROOT%\frontend\src\components\UploadArea.jsx
type nul > %ROOT%\frontend\src\components\GeneratedDocs.jsx
type nul > %ROOT%\frontend\src\components\Chatbot.jsx
type nul > %ROOT%\frontend\src\components\DownloadButtons.jsx
type nul > %ROOT%\frontend\src\components\ADOPushButton.jsx
type nul > %ROOT%\frontend\src\services\api.js

type nul > %ROOT%\frontend\package.json

echo Folder structure created successfully!
pause
