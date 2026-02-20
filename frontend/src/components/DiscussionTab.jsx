import React, { useState, useEffect } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Paper,
  Alert,
  CircularProgress,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material'
import { Send, CheckCircle } from '@mui/icons-material'
import { discussIdea, getAvailableModels } from '../services/api'

const DiscussionTab = ({ selectedIdea, onFinalize, ollamaConnected }) => {
  const [question, setQuestion] = useState('')
  const [conversation, setConversation] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [models, setModels] = useState([])
  const [selectedModel, setSelectedModel] = useState('')

  useEffect(() => {
    if (ollamaConnected) {
      loadModels()
    }
  }, [ollamaConnected])

  const loadModels = async () => {
    try {
      const availableModels = await getAvailableModels()
      setModels(availableModels)
      if (availableModels.length > 0) {
        setSelectedModel(availableModels[0])
      }
    } catch (error) {
      console.error('Failed to load models:', error)
    }
  }

  const handleDiscuss = async () => {
    if (!question.trim()) return
    if (!ollamaConnected) {
      setError('Ollama is not connected')
      return
    }
    if (!selectedModel) {
      setError('Please select an Ollama model')
      return
    }

    const userQuestion = question.trim()
    setQuestion('')
    setLoading(true)
    setError(null)

    // Add user question to conversation
    const newConversation = [...conversation, { role: 'user', content: userQuestion }]
    setConversation(newConversation)

    try {
      const response = await discussIdea(selectedIdea, userQuestion, conversation, selectedModel)
      setConversation([...newConversation, { role: 'assistant', content: response }])
    } catch (err) {
      setError(err.message)
      setConversation(newConversation.slice(0, -1)) // Remove user question on error
    } finally {
      setLoading(false)
    }
  }

  const handleFinalize = () => {
    if (selectedIdea) {
      onFinalize(selectedIdea)
    }
  }

  if (!selectedIdea) {
    return (
      <Alert severity="info">
        No idea selected. Please go to the "Generate Ideas" tab and select an idea first.
      </Alert>
    )
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Refine Your Video Idea
      </Typography>

      <Card elevation={2} sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ mb: 1 }}>
            Selected Idea
          </Typography>
          <Paper
            variant="outlined"
            sx={{
              p: 2,
              bgcolor: 'primary.light',
              color: 'white',
              borderRadius: 1,
            }}
          >
            <Typography>{selectedIdea}</Typography>
          </Paper>
        </CardContent>
      </Card>

      <Card elevation={2} sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
            Discussion History
          </Typography>
          <Paper
            variant="outlined"
            sx={{
              p: 2,
              minHeight: 300,
              maxHeight: 400,
              overflow: 'auto',
              bgcolor: 'background.paper',
            }}
          >
            {conversation.length === 0 ? (
              <Typography color="text.secondary" sx={{ fontStyle: 'italic' }}>
                Start discussing your idea below...
              </Typography>
            ) : (
              conversation.map((msg, index) => (
                <Box
                  key={index}
                  sx={{
                    mb: 2,
                    display: 'flex',
                    justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  }}
                >
                  <Chip
                    label={msg.content}
                    color={msg.role === 'user' ? 'primary' : 'default'}
                    sx={{
                      maxWidth: '70%',
                      '& .MuiChip-label': {
                        whiteSpace: 'normal',
                        wordBreak: 'break-word',
                      },
                    }}
                  />
                </Box>
              ))
            )}
            {loading && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                <CircularProgress size={24} />
              </Box>
            )}
          </Paper>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Card elevation={2} sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
            Your Question or Refinement
          </Typography>
          
          {models.length > 0 ? (
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Ollama Model</InputLabel>
              <Select
                value={selectedModel}
                label="Ollama Model"
                onChange={(e) => setSelectedModel(e.target.value)}
              >
                {models.map((model) => (
                  <MenuItem key={model} value={model}>
                    {model}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          ) : ollamaConnected ? (
            <Alert severity="warning" sx={{ mb: 2 }}>
              No Ollama models found. Please pull a model first (e.g., ollama pull llama3)
            </Alert>
          ) : null}

          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              fullWidth
              multiline
              rows={2}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask questions or request refinements..."
              onKeyPress={(e) => {
                if (e.key === 'Enter' && e.ctrlKey) {
                  handleDiscuss()
                }
              }}
            />
            <Button
              variant="contained"
              color="warning"
              startIcon={<Send />}
              onClick={handleDiscuss}
              disabled={loading || !question.trim() || !ollamaConnected || !selectedModel}
              sx={{ minWidth: 120 }}
            >
              Discuss
            </Button>
          </Box>
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
            Press Ctrl+Enter to send
          </Typography>
        </CardContent>
      </Card>

      <Button
        variant="contained"
        color="secondary"
        size="large"
        startIcon={<CheckCircle />}
        onClick={handleFinalize}
        disabled={!selectedIdea}
        sx={{ minWidth: 300 }}
      >
        Finalize Idea & Generate Script
      </Button>
    </Box>
  )
}

export default DiscussionTab
