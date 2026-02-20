import React, { useState } from 'react'
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
  FormControlLabel,
  Checkbox,
  Paper,
  Alert,
  CircularProgress,
  Chip,
  Divider,
} from '@mui/material'
import { PlayArrow, Save, Movie, Refresh } from '@mui/icons-material'
import { generateScript, generateSeries, getAvailableModels } from '../services/api'

const ScriptGenerator = ({ finalizedIdea, ollamaConnected }) => {
  const [topic, setTopic] = useState(finalizedIdea || '')
  const [videoLength, setVideoLength] = useState('1.0')
  const [tone, setTone] = useState('Professional')
  const [language, setLanguage] = useState('English')
  const [keywords, setKeywords] = useState('')
  const [includeImages, setIncludeImages] = useState(false)
  const [imageType, setImageType] = useState('descriptions')
  const [script, setScript] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [scriptStats, setScriptStats] = useState(null)
  const [models, setModels] = useState([])
  const [selectedModel, setSelectedModel] = useState('')

  const [seriesEpisodes, setSeriesEpisodes] = useState('3')
  const [generatingSeries, setGeneratingSeries] = useState(false)

  React.useEffect(() => {
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

  React.useEffect(() => {
    if (finalizedIdea) {
      setTopic(finalizedIdea)
    }
  }, [finalizedIdea])

  const handleGenerate = async () => {
    if (!topic.trim()) {
      setError('Please enter a topic')
      return
    }
    if (!ollamaConnected) {
      setError('Ollama is not connected')
      return
    }

    setLoading(true)
    setError(null)
    const progressMsg = language !== 'English' 
      ? 'Generating script in ' + language + '... This may take 2-3 minutes. Please wait...'
      : 'Generating script... Please wait...'
    setScript(progressMsg)

    if (!selectedModel) {
      setError('Please select an Ollama model')
      setLoading(false)
      return
    }

    try {
      const result = await generateScript({
        idea: topic,
        keywords,
        videoLengthMinutes: parseFloat(videoLength),
        tone,
        language,
        model: selectedModel,
        includeImages,
        imageType,
      })
      setScript(result.script)
      setScriptStats({
        actualChars: result.actual_chars,
        targetChars: result.target_chars,
        isValid: result.is_valid_length,
      })
    } catch (err) {
      console.error('Generate script error:', err)
      const errorMsg = err.message || 'Failed to generate script. Please check that the backend is running on port 5000.'
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateSeries = async () => {
    if (!topic.trim()) {
      setError('Please enter a topic')
      return
    }
    if (!ollamaConnected) {
      setError('Ollama is not connected')
      return
    }

    try {
      const numEp = parseInt(seriesEpisodes)
      if (numEp < 1 || numEp > 10) {
        setError('Number of episodes must be between 1 and 10')
        return
      }
    } catch (e) {
      setError('Please enter a valid number of episodes')
      return
    }

    setGeneratingSeries(true)
    setError(null)
    const numEp = parseInt(seriesEpisodes)
    const estimatedTime = language !== 'English' ? numEp * 2 : numEp * 1
    setScript(`Generating ${numEp} episode${numEp > 1 ? 's' : ''}... This may take ${estimatedTime}-${estimatedTime + 2} minutes${language !== 'English' ? ' (longer for non-English languages)' : ''}.`)

    if (!selectedModel) {
      setError('Please select an Ollama model')
      setGeneratingSeries(false)
      return
    }

    try {
      const result = await generateSeries({
        idea: topic,
        numEpisodes: parseInt(seriesEpisodes),
        keywords,
        videoLengthMinutes: parseFloat(videoLength),
        tone,
        language,
        model: selectedModel,
        includeImages,
        imageType,
      })
      setScript(result.combinedScript)
      setScriptStats(null)
    } catch (err) {
      console.error('Generate series error:', err)
      const errorMsg = err.message || 'Failed to generate series. Please check that the backend is running on port 5000.'
      setError(errorMsg)
    } finally {
      setGeneratingSeries(false)
    }
  }

  const handleSave = () => {
    if (!script) return

    const blob = new Blob([script], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `script_${topic.replace(/\s+/g, '_')}_${Date.now()}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const targetChars = Math.round(parseFloat(videoLength) * 600)

  return (
    <Box sx={{ display: 'flex', gap: 3, flexDirection: { xs: 'column', lg: 'row' } }}>
      {/* Left Panel - Inputs */}
      <Box sx={{ flex: { xs: 1, lg: '0 0 450px' } }}>
        <Typography variant="h5" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
          Create Your Video Script
        </Typography>

        <Card elevation={2} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Video Topic / Idea
            </Typography>
            <TextField
              fullWidth
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter topic or use finalized idea"
              sx={{ mb: 1 }}
            />
            {finalizedIdea && (
              <Chip
                label={`Finalized: ${finalizedIdea}`}
                color="success"
                size="small"
                sx={{ mt: 1 }}
              />
            )}
          </CardContent>
        </Card>

        <Card elevation={2} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Script Parameters
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                <FormControl fullWidth>
                  <InputLabel>Ollama Model</InputLabel>
                  <Select
                    value={selectedModel}
                    label="Ollama Model"
                    onChange={(e) => setSelectedModel(e.target.value)}
                    disabled={models.length === 0}
                  >
                    {models.length === 0 ? (
                      <MenuItem disabled>No models available</MenuItem>
                    ) : (
                      models.map((model) => (
                        <MenuItem key={model} value={model}>
                          {model}
                        </MenuItem>
                      ))
                    )}
                  </Select>
                </FormControl>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={loadModels}
                  startIcon={<Refresh />}
                  sx={{ minWidth: 100, height: 56 }}
                >
                  Refresh
                </Button>
              </Box>
              {models.length === 0 && (
                <Alert severity="warning" sx={{ mt: 1 }}>
                  No Ollama models found. Please pull a model first (e.g., ollama pull llama3)
                </Alert>
              )}

              <TextField
                label="Video Length (minutes)"
                type="number"
                value={videoLength}
                onChange={(e) => setVideoLength(e.target.value)}
                inputProps={{ min: 0.1, max: 60, step: 0.1 }}
                helperText={`Target: ${targetChars} characters`}
              />

              <FormControl fullWidth>
                <InputLabel>Tone/Style</InputLabel>
                <Select value={tone} label="Tone/Style" onChange={(e) => setTone(e.target.value)}>
                  <MenuItem value="Professional">Professional</MenuItem>
                  <MenuItem value="Casual">Casual</MenuItem>
                  <MenuItem value="Educational">Educational</MenuItem>
                </Select>
              </FormControl>

              <FormControl fullWidth>
                <InputLabel>Script Language</InputLabel>
                <Select value={language} label="Script Language" onChange={(e) => setLanguage(e.target.value)}>
                  <MenuItem value="English">English</MenuItem>
                  <MenuItem value="Urdu">Urdu (اردو)</MenuItem>
                  <MenuItem value="Hindi">Hindi (हिंदी)</MenuItem>
                  <MenuItem value="Spanish">Spanish (Español)</MenuItem>
                  <MenuItem value="French">French (Français)</MenuItem>
                  <MenuItem value="Arabic">Arabic (العربية)</MenuItem>
                  <MenuItem value="Chinese">Chinese (中文)</MenuItem>
                </Select>
              </FormControl>

              <TextField
                label="Additional Keywords"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                placeholder="Optional keywords or points"
              />

              <FormControlLabel
                control={
                  <Checkbox
                    checked={includeImages}
                    onChange={(e) => setIncludeImages(e.target.checked)}
                  />
                }
                label="Include image descriptions and visual cues"
              />

              {includeImages && (
                <FormControl fullWidth>
                  <InputLabel>Image Type</InputLabel>
                  <Select
                    value={imageType}
                    label="Image Type"
                    onChange={(e) => setImageType(e.target.value)}
                  >
                    <MenuItem value="descriptions">Descriptions</MenuItem>
                    <MenuItem value="AI prompts">AI Prompts</MenuItem>
                    <MenuItem value="both">Both</MenuItem>
                  </Select>
                </FormControl>
              )}
            </Box>
          </CardContent>
        </Card>

        <Card elevation={2} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Generate Series
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
              <TextField
                label="Episodes"
                type="number"
                value={seriesEpisodes}
                onChange={(e) => setSeriesEpisodes(e.target.value)}
                inputProps={{ min: 1, max: 10 }}
                sx={{ width: 120 }}
              />
              <Button
                variant="contained"
                color="secondary"
                startIcon={<Movie />}
                onClick={handleGenerateSeries}
                disabled={generatingSeries || !ollamaConnected}
                sx={{ flex: 1 }}
              >
                {generatingSeries ? (
                  <CircularProgress size={20} color="inherit" />
                ) : (
                  'Generate Series'
                )}
              </Button>
            </Box>
          </CardContent>
        </Card>

        <Button
          variant="contained"
          color="success"
          size="large"
          fullWidth
          startIcon={<PlayArrow />}
          onClick={handleGenerate}
          disabled={loading || !ollamaConnected}
          sx={{ mb: 2 }}
        >
          {loading ? <CircularProgress size={24} color="inherit" /> : 'Generate Script'}
        </Button>

        {error && <Alert severity="error">{error}</Alert>}
      </Box>

      {/* Right Panel - Script Preview */}
      <Box sx={{ flex: 1 }}>
        <Card elevation={2} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
          <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">Generated Script</Typography>
              {scriptStats && (
                <Chip
                  label={`${scriptStats.actualChars}/${scriptStats.targetChars} chars`}
                  color={scriptStats.isValid ? 'success' : 'warning'}
                  size="small"
                />
              )}
            </Box>

            {script ? (
              <>
                <Paper
                  variant="outlined"
                  sx={{
                    flex: 1,
                    p: 2,
                    overflow: 'auto',
                    bgcolor: 'background.paper',
                    fontFamily: 'monospace',
                    fontSize: '0.95rem',
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                  }}
                >
                  {script}
                </Paper>
                <Box sx={{ mt: 2 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<Save />}
                    onClick={handleSave}
                    fullWidth
                  >
                    Save Script
                  </Button>
                </Box>
              </>
            ) : (
              <Paper
                variant="outlined"
                sx={{
                  flex: 1,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  bgcolor: 'background.default',
                }}
              >
                <Typography color="text.secondary" sx={{ fontStyle: 'italic' }}>
                  {loading || generatingSeries
                    ? 'Generating script... Please wait...'
                    : 'Generated script will appear here'}
                </Typography>
              </Paper>
            )}
          </CardContent>
        </Card>
      </Box>
    </Box>
  )
}

export default ScriptGenerator
