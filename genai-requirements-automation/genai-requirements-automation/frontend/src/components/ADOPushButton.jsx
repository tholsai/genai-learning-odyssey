import { useState } from 'react'
import { pushToADO } from '../services/api'

const ADOPushButton = ({ generatedArtifacts }) => {
  const [pushing, setPushing] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const handlePush = async () => {
    if (!generatedArtifacts || Object.keys(generatedArtifacts).length === 0) {
      setError('No artifacts to push. Please generate artifacts first.')
      return
    }

    setPushing(true)
    setError(null)
    setResult(null)

    try {
      const artifactTypes = Object.keys(generatedArtifacts)
      const response = await pushToADO(artifactTypes, 'User Story')
      setResult(response)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Push to Azure DevOps failed')
    } finally {
      setPushing(false)
    }
  }

  return (
    <div className="ado-push">
      <h2>Push to Azure DevOps</h2>
      <button
        onClick={handlePush}
        disabled={pushing || !generatedArtifacts || Object.keys(generatedArtifacts).length === 0}
        className="ado-btn"
      >
        {pushing ? 'Pushing...' : 'Push Artifacts to Azure DevOps'}
      </button>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="success">
          <p>✓ {result.message}</p>
          {result.work_items_created && result.work_items_created.length > 0 && (
            <div>
              <h4>Created Work Items:</h4>
              <ul>
                {result.work_items_created.map((item, idx) => (
                  <li key={idx}>
                    <a href={item.url} target="_blank" rel="noopener noreferrer">
                      {item.title} (ID: {item.id})
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ADOPushButton

