import React, { useState, useEffect } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  CircularProgress,
  Alert,
  Paper,
} from '@mui/material'
import { AutoAwesome, Refresh } from '@mui/icons-material'
import { getAvailableModels, generateIdeas } from '../services/api'

const IdeaGenerator = ({ onIdeaSelect, ollamaConnected }) => {
  const [models, setModels] = useState([])
  const [selectedModel, setSelectedModel] = useState('llama3')
  const [category, setCategory] = useState('Any')
  const [ideas, setIdeas] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (ollamaConnected) {
      loadModels()
    }
  }, [ollamaConnected])

  const loadModels = async () => {
    try {
      const availableModels = await getAvailableModels()
      setModels(availableModels)
      if (availableModels.length > 0 && !availableModels.includes(selectedModel)) {
        setSelectedModel(availableModels[0])
      }
    } catch (error) {
      console.error('Failed to load models:', error)
    }
  }

  const handleGenerate = async () => {
    if (!ollamaConnected) {
      setError('Ollama is not connected')
      return
    }

    setLoading(true)
    setError(null)
    setIdeas([])

    try {
      const generatedIdeas = await generateIdeas(category, selectedModel)
      setIdeas(generatedIdeas)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSelectIdea = (idea) => {
    onIdeaSelect(idea)
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Discover Trending Video Topics
      </Typography>

      <Card elevation={2} sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
            Configuration
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 2 }}>
            <FormControl sx={{ minWidth: 200 }}>
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

            <Button
              startIcon={<Refresh />}
              onClick={loadModels}
              variant="outlined"
              sx={{ height: 56 }}
            >
              Refresh Models
            </Button>

            <FormControl sx={{ minWidth: 200 }}>
              <InputLabel>Topic Category</InputLabel>
              <Select
                value={category}
                label="Topic Category"
                onChange={(e) => setCategory(e.target.value)}
              >
                <MenuItem value="Any">Any</MenuItem>
                <MenuItem value="AI">AI</MenuItem>
                <MenuItem value="WordPress">WordPress</MenuItem>
                <MenuItem value="Robotics">Robotics</MenuItem>
                <MenuItem value="General Tech">General Tech</MenuItem>
              </Select>
            </FormControl>
          </Box>

          <Button
            variant="contained"
            color="success"
            size="large"
            startIcon={<AutoAwesome />}
            onClick={handleGenerate}
            disabled={loading || !ollamaConnected}
            sx={{ minWidth: 200 }}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Generate Ideas'}
          </Button>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {ideas.length > 0 && (
        <Card elevation={2}>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
              Generated Ideas
            </Typography>
            <Paper variant="outlined">
              <List>
                {ideas.map((idea, index) => (
                  <ListItem key={index} disablePadding>
                    <ListItemButton onClick={() => handleSelectIdea(idea)}>
                      <ListItemText
                        primary={idea}
                        primaryTypographyProps={{
                          sx: { fontWeight: 500 },
                        }}
                      />
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </Paper>
            <Box sx={{ mt: 2 }}>
              <Button
                variant="outlined"
                color="primary"
                onClick={() => ideas.length > 0 && handleSelectIdea(ideas[0])}
                disabled={ideas.length === 0}
              >
                Select First Idea & Continue
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}
    </Box>
  )
}

export default IdeaGenerator
