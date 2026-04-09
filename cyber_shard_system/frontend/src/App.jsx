import { Routes, Route } from "react-router-dom"
import Layout from "./components/Layout"
import Records from "./pages/Records"
import DocumentView from "./pages/DocumentView"
import SecurityConsole from "./pages/SecurityConsole"
import ActivityLogs from "./pages/ActivityLogs"

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Records />} />
        <Route path="/document/:id" element={<DocumentView />} />
        <Route path="/security" element={<SecurityConsole />} />
        <Route path="/logs" element={<ActivityLogs />} />
      </Routes>
    </Layout>
  )
}

export default App