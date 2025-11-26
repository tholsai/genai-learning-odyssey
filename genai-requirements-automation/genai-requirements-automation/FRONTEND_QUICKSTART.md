# Frontend Quick Start Guide

## How to Run the Frontend

### Step 1: Install Node.js Dependencies

Open a terminal in the `frontend` directory and run:

```bash
cd frontend
npm install
```

This will install all required packages (React, Vite, Axios, etc.)

### Step 2: Make Sure Backend is Running

In a separate terminal, ensure your FastAPI backend is running:

```bash
cd backend
uv run uvicorn app:app --reload
```

The backend should be running on **http://127.0.0.1:8000**

### Step 3: Start the Frontend

In the frontend terminal, run:

```bash
npm run dev
```

You should see output like:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Step 4: Open in Browser

Open your browser and navigate to:
**http://localhost:3000**

## What You'll See

The frontend provides a beautiful UI with:

1. **Upload Section**: Drag and drop or select PDF/DOCX files
2. **Generate Section**: Select artifact types and generate requirements
3. **Download Buttons**: Download generated artifacts
4. **Chatbot**: Ask questions about your requirements
5. **Azure DevOps Push**: Push artifacts to ADO (if configured)

## Complete Workflow

1. **Upload Document**:
   - Click "Choose PDF or DOCX file"
   - Select your functional specification
   - Click "Upload"
   - Wait for upload confirmation

2. **Generate Artifacts**:
   - Select which artifacts to generate (Epic, Stories, Use Cases, TDD, Data Model)
   - Choose output format (DOCX or PDF)
   - Click "Generate Artifacts"
   - Wait 30-60 seconds for generation

3. **Download Files**:
   - Click download buttons for each generated artifact
   - Files will download to your Downloads folder

4. **Use Chatbot**:
   - Type questions in the chat input
   - Enable/disable RAG for context-aware answers
   - Get instant responses about your requirements

5. **Push to Azure DevOps** (Optional):
   - After generating artifacts
   - Click "Push Artifacts to Azure DevOps"
   - Configure ADO settings in backend `.env` first

## Troubleshooting

### "Cannot connect to backend"
- Ensure backend is running on port 8000
- Check `http://127.0.0.1:8000/health` in browser
- Verify CORS is enabled in backend

### "Port 3000 already in use"
- Change port in `vite.config.js`:
  ```js
  server: {
    port: 3001, // or any available port
  }
  ```

### "npm install fails"
- Make sure Node.js 18+ is installed
- Try deleting `node_modules` and `package-lock.json`, then run `npm install` again
- Use `npm install --legacy-peer-deps` if needed

### Frontend loads but API calls fail
- Check browser console (F12) for errors
- Verify backend is running
- Check network tab for failed requests
- Ensure Ollama is running and Mistral model is available

## Alternative: Using Yarn or pnpm

If you prefer yarn:
```bash
yarn install
yarn dev
```

If you prefer pnpm:
```bash
pnpm install
pnpm dev
```

## Production Build

To build for production:
```bash
npm run build
```

The built files will be in the `dist/` directory.

## Features

- ✅ Modern React with Hooks
- ✅ Beautiful gradient UI design
- ✅ Responsive layout
- ✅ Real-time file upload
- ✅ Progress indicators
- ✅ Error handling
- ✅ Download functionality
- ✅ Interactive chatbot
- ✅ Azure DevOps integration

Enjoy using the GenAI Requirements Automation frontend! 🚀

