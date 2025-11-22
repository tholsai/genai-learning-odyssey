import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutes default timeout for all requests
})

export const uploadDocument = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const generateArtifacts = async (specText, specFilePath, artifactTypes, outputFormat = 'docx') => {
  const payload = {
    artifact_types: artifactTypes,
    output_format: outputFormat,
  }
  
  if (specFilePath) {
    payload.spec_file_path = specFilePath
  } else if (specText) {
    payload.spec_text = specText
  }
  
  const response = await api.post('/generate', payload, {
    timeout: 900000, // 15 minutes - local models can be slower
  })
  return response.data
}

export const downloadDocument = async (docType, artifactType = null) => {
  const params = artifactType ? { artifact_type: artifactType } : {}
  const response = await api.get(`/download/${docType}`, {
    params,
    responseType: 'blob',
  })
  return response.data
}

export const chat = async (message, useRag = true) => {
  const response = await api.post('/chat', {
    message,
    use_rag: useRag,
  }, {
    timeout: 300000, // 5 minutes - local models can be slower
  })
  return response.data
}

export const pushToADO = async (artifactTypes, workItemType = 'User Story') => {
  const response = await api.post('/ado/push', {
    artifact_types: artifactTypes,
    work_item_type: workItemType,
  })
  return response.data
}

export default api

