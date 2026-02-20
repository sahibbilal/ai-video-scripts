import React, { useState, useEffect } from 'react'
import {
  Container,
  Box,
  AppBar,
  Toolbar,
  Typography,
  Tabs,
  Tab,
  Paper,
  Alert,
  CircularProgress,
} from '@mui/material'
import { VideoLibrary, Chat, Description } from '@mui/icons-material'
import IdeaGenerator from './components/IdeaGenerator'
import DiscussionTab from './components/DiscussionTab'
import ScriptGenerator from './components/ScriptGenerator'
import { checkOllamaConnection } from './services/api'

function App() {
  const [activeTab, setActiveTab] = useState(0)
  const [ollamaStatus, setOllamaStatus] = useState({ connected: false, loading: true })
  const [selectedIdea, setSelectedIdea] = useState(null)
  const [finalizedIdea, setFinalizedIdea] = useState(null)

  useEffect(() => {
    checkConnection()
    // Check connection every 10 seconds
    const interval = setInterval(checkConnection, 10000)
    return () => clearInterval(interval)
  }, [])

  const checkConnection = async () => {
    try {
      const status = await checkOllamaConnection()
      setOllamaStatus({ connected: status.connected, loading: false })
    } catch (error) {
      setOllamaStatus({ connected: false, loading: false })
    }
  }

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue)
  }

  const handleIdeaSelect = (idea) => {
    setSelectedIdea(idea)
    setActiveTab(1) // Switch to discussion tab
  }

  const handleIdeaFinalize = (idea) => {
    setFinalizedIdea(idea)
    setActiveTab(2) // Switch to script generation tab
  }

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="static" elevation={2}>
        <Toolbar>
          <VideoLibrary sx={{ mr: 2 }} />
          <Typography variant="h5" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            Video Script Generator
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {ollamaStatus.loading ? (
              <CircularProgress size={20} color="inherit" />
            ) : (
              <Box
                sx={{
                  width: 10,
                  height: 10,
                  borderRadius: '50%',
                  bgcolor: ollamaStatus.connected ? 'success.main' : 'error.main',
                  mr: 1,
                }}
              />
            )}
            <Typography variant="body2">
              {ollamaStatus.connected ? 'Ollama Connected' : 'Ollama Not Connected'}
            </Typography>
          </Box>
        </Toolbar>
      </AppBar>

      {!ollamaStatus.connected && !ollamaStatus.loading && (
        <Alert severity="warning" sx={{ m: 2 }}>
          Ollama is not connected. Please make sure Ollama is running on your system.
        </Alert>
      )}

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Paper elevation={3} sx={{ overflow: 'hidden' }}>
          <Tabs
            value={activeTab}
            onChange={handleTabChange}
            variant="fullWidth"
            sx={{
              borderBottom: 1,
              borderColor: 'divider',
              '& .MuiTab-root': {
                minHeight: 72,
                fontSize: '1rem',
                fontWeight: 600,
              },
            }}
          >
            <Tab
              icon={<VideoLibrary />}
              iconPosition="start"
              label="Generate Ideas"
              sx={{ textTransform: 'none' }}
            />
            <Tab
              icon={<Chat />}
              iconPosition="start"
              label="Discuss & Refine"
              sx={{ textTransform: 'none' }}
            />
            <Tab
              icon={<Description />}
              iconPosition="start"
              label="Generate Script"
              sx={{ textTransform: 'none' }}
            />
          </Tabs>

          <Box sx={{ p: 3 }}>
            {activeTab === 0 && (
              <IdeaGenerator
                onIdeaSelect={handleIdeaSelect}
                ollamaConnected={ollamaStatus.connected}
              />
            )}
            {activeTab === 1 && (
              <DiscussionTab
                selectedIdea={selectedIdea}
                onFinalize={handleIdeaFinalize}
                ollamaConnected={ollamaStatus.connected}
              />
            )}
            {activeTab === 2 && (
              <ScriptGenerator
                finalizedIdea={finalizedIdea}
                ollamaConnected={ollamaStatus.connected}
              />
            )}
          </Box>
        </Paper>
      </Container>
    </Box>
  )
}

export default App
