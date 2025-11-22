# Frontend - GenAI Requirements Automation

React frontend for the GenAI Requirements Automation system.

## Setup

### Prerequisites
- Node.js 18+ and npm (or yarn/pnpm)

### Installation

1. Install dependencies:
```bash
cd frontend
npm install
```

Or using yarn:
```bash
yarn install
```

Or using pnpm:
```bash
pnpm install
```

## Running the Frontend

### Development Mode
```bash
npm run dev
```

The frontend will be available at: **http://localhost:3000**

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## Configuration

The frontend is configured to connect to the FastAPI backend at:
- **Backend URL**: `http://127.0.0.1:8000`

This is configured in:
- `vite.config.js` - Proxy configuration
- `src/services/api.js` - API base URL

## Features

1. **Upload Documents**: Upload PDF/DOCX functional specifications
2. **Generate Artifacts**: Generate epics, stories, use cases, TDD tests, and data models
3. **Download Files**: Download generated artifacts as DOCX or PDF
4. **AI Chatbot**: Interactive chatbot for questions about requirements
5. **Azure DevOps Integration**: Push generated artifacts to Azure DevOps

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── UploadArea.jsx       # Document upload component
│   │   ├── GeneratedDocs.jsx    # Artifact generation component
│   │   ├── Chatbot.jsx          # AI chatbot component
│   │   └── ADOPushButton.jsx    # Azure DevOps push component
│   ├── services/
│   │   └── api.js               # API service layer
│   ├── App.jsx                  # Main app component
│   ├── App.css                  # App styles
│   ├── main.jsx                 # Entry point
│   └── index.css                # Global styles
├── index.html                   # HTML template
├── vite.config.js              # Vite configuration
└── package.json                 # Dependencies
```

## Usage

1. **Start the Backend** (in a separate terminal):
   ```bash
   cd backend
   uv run uvicorn app:app --reload
   ```

2. **Start the Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open Browser**: Navigate to http://localhost:3000

4. **Workflow**:
   - Upload a PDF/DOCX specification
   - Select artifact types to generate
   - Click "Generate Artifacts"
   - Download generated files
   - Use chatbot for questions
   - Push to Azure DevOps (optional)

## Troubleshooting

### Frontend can't connect to backend
- Ensure backend is running on http://127.0.0.1:8000
- Check CORS settings in backend (should be enabled)
- Verify proxy configuration in `vite.config.js`

### Port 3000 already in use
- Change port in `vite.config.js`:
  ```js
  server: {
    port: 3001, // Change to available port
  }
  ```

### API errors
- Check backend logs for errors
- Verify Ollama is running and Mistral model is available
- Check network tab in browser DevTools

