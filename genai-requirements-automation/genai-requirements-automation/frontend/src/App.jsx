import { useState } from 'react'
import UploadArea from './components/UploadArea'
import GeneratedDocs from './components/GeneratedDocs'
import Chatbot from './components/Chatbot'
import ADOPushButton from './components/ADOPushButton'
import './App.css'

function App() {
  const [uploadedFile, setUploadedFile] = useState(null)
  const [generatedArtifacts, setGeneratedArtifacts] = useState(null)

  const handleUploadSuccess = (result) => {
    setUploadedFile(result.file_path)
  }

  const handleGenerationSuccess = (results) => {
    setGeneratedArtifacts(results.artifacts)
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🚀 GenAI Requirements Automation</h1>
        <p>Upload specifications, generate artifacts, and push to Azure DevOps</p>
      </header>

      <main className="App-main">
        <section className="section">
          <UploadArea onUploadSuccess={handleUploadSuccess} />
        </section>

        {uploadedFile && (
          <section className="section">
            <GeneratedDocs 
              uploadedFilePath={uploadedFile}
              onGenerationSuccess={handleGenerationSuccess}
            />
          </section>
        )}

        {generatedArtifacts && (
          <section className="section">
            <ADOPushButton generatedArtifacts={generatedArtifacts} />
          </section>
        )}

        <section className="section">
          <Chatbot />
        </section>
      </main>

      <footer className="App-footer">
        <p>GenAI Requirements Automation API - FastAPI Backend</p>
      </footer>
    </div>
  )
}

export default App

