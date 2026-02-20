import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes for long operations (especially non-English languages)
})

export const checkOllamaConnection = async () => {
  try {
    const response = await api.get('/ollama/check')
    return response.data
  } catch (error) {
    return { connected: false }
  }
}

export const getAvailableModels = async () => {
  try {
    const response = await api.get('/ollama/models')
    return response.data.models || []
  } catch (error) {
    return []
  }
}

export const generateIdeas = async (category, model) => {
  try {
    const response = await api.post('/ideas/generate', { category, model })
    return response.data.ideas || []
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to generate ideas')
  }
}

export const discussIdea = async (idea, question, conversationHistory, model) => {
  try {
    const response = await api.post('/discuss', {
      idea,
      question,
      conversationHistory,
      model,
    })
    return response.data.response
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to discuss idea')
  }
}

export const generateScript = async (scriptData) => {
  try {
    console.log('Sending script generation request:', scriptData)
    const response = await api.post('/script/generate', scriptData)
    return response.data
  } catch (error) {
    console.error('Script generation error:', error)
    const errorMessage = error.response?.data?.error || error.message || 'Failed to generate script'
    throw new Error(errorMessage)
  }
}

export const generateSeries = async (seriesData) => {
  try {
    const response = await api.post('/script/series', seriesData)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to generate series')
  }
}
