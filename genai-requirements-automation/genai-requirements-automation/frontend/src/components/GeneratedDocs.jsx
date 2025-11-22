import { useState } from 'react'
import { generateArtifacts, downloadDocument } from '../services/api'

const GeneratedDocs = ({ uploadedFilePath, onGenerationSuccess }) => {
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState(null)
  const [results, setResults] = useState(null)
  const [selectedArtifacts, setSelectedArtifacts] = useState({
    epic: true,
    stories: true,
    use_cases: true,
    tdd: true,
    data_model: true,
  })
  const [outputFormat, setOutputFormat] = useState('docx')

  const handleGenerate = async () => {
    if (!uploadedFilePath) {
      setError('Please upload a document first')
      return
    }

    const artifactTypes = Object.entries(selectedArtifacts)
      .filter(([_, selected]) => selected)
      .map(([type, _]) => type)

    if (artifactTypes.length === 0) {
      setError('Please select at least one artifact type')
      return
    }

    setGenerating(true)
    setError(null)
    setResults(null)

    try {
      const result = await generateArtifacts(
        null,
        uploadedFilePath,
        artifactTypes,
        outputFormat
      )
      setResults(result)
      if (onGenerationSuccess) {
        onGenerationSuccess(result)
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Generation failed')
    } finally {
      setGenerating(false)
    }
  }

  const handleDownload = async (artifactType) => {
    try {
      const blob = await downloadDocument(outputFormat, artifactType)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${artifactType}.${outputFormat}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      alert('Download failed: ' + (err.response?.data?.detail || err.message))
    }
  }

  return (
    <div className="generated-docs">
      <h2>Generate Requirements Artifacts</h2>
      
      <div className="artifact-selection">
        <h3>Select Artifact Types:</h3>
        {Object.keys(selectedArtifacts).map((type) => (
          <label key={type} className="checkbox-label">
            <input
              type="checkbox"
              checked={selectedArtifacts[type]}
              onChange={(e) =>
                setSelectedArtifacts({
                  ...selectedArtifacts,
                  [type]: e.target.checked,
                })
              }
            />
            {type.replace('_', ' ').toUpperCase()}
          </label>
        ))}
      </div>

      <div className="format-selection">
        <label>
          Output Format:
          <select
            value={outputFormat}
            onChange={(e) => setOutputFormat(e.target.value)}
          >
            <option value="docx">DOCX</option>
            <option value="pdf">PDF</option>
          </select>
        </label>
      </div>

      <button
        onClick={handleGenerate}
        disabled={generating || !uploadedFilePath}
        className="generate-btn"
      >
        {generating ? 'Generating... (This may take 30-60 seconds)' : 'Generate Artifacts'}
      </button>

      {error && <div className="error">{error}</div>}

      {results && (
        <div className="results">
          <h3>✓ Generation Complete!</h3>
          <p>{results.message}</p>
          <div className="download-buttons">
            {Object.keys(results.file_paths).map((artifactType) => (
              <button
                key={artifactType}
                onClick={() => handleDownload(artifactType)}
                className="download-btn"
              >
                Download {artifactType.replace('_', ' ').toUpperCase()}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default GeneratedDocs

