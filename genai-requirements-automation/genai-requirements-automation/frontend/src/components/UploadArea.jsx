import { useState } from 'react'
import { uploadDocument } from '../services/api'

const UploadArea = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState(null)
  const [uploadResult, setUploadResult] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      if (selectedFile.type === 'application/pdf' || 
          selectedFile.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        setFile(selectedFile)
        setError(null)
      } else {
        setError('Please upload a PDF or DOCX file')
        setFile(null)
      }
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first')
      return
    }

    setUploading(true)
    setError(null)

    try {
      const result = await uploadDocument(file)
      setUploadResult(result)
      if (onUploadSuccess) {
        onUploadSuccess(result)
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="upload-area">
      <h2>Upload Functional Specification</h2>
      <div className="upload-box">
        <input
          type="file"
          accept=".pdf,.docx,.doc"
          onChange={handleFileChange}
          disabled={uploading}
          id="file-input"
        />
        <label htmlFor="file-input" className="file-label">
          {file ? file.name : 'Choose PDF or DOCX file'}
        </label>
        <button 
          onClick={handleUpload} 
          disabled={!file || uploading}
          className="upload-btn"
        >
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </div>
      
      {error && <div className="error">{error}</div>}
      
      {uploadResult && (
        <div className="success">
          <p>✓ Upload successful!</p>
          <p>File: {uploadResult.file_name}</p>
          <p>File path: {uploadResult.file_path}</p>
        </div>
      )}
    </div>
  )
}

export default UploadArea

