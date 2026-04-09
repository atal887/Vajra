import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import { RecordsProvider } from './context/RecordsContext'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <RecordsProvider>
        <App />
      </RecordsProvider>
    </BrowserRouter>
  </StrictMode>,
)
