import { useState, useEffect } from "react"
import { useNavigate, useParams } from "react-router-dom"
import * as api from "../services/api"
import { useRecords } from "../context/RecordsContext"

export default function DocumentView() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { getDocument, fetchDocuments } = useRecords()

  const [content, setContent] = useState("")
  const [status, setStatus] = useState("active")
  const [isSaving, setIsSaving] = useState(false)
  const [isRestoring, setIsRestoring] = useState(false)
  const [error, setError] = useState(null)

  const doc = getDocument(id)

  useEffect(() => {
    loadDocument()
  }, [id])

  const loadDocument = async () => {
    try {
      const res = await api.viewDocument(id)
      if (res.error) {
        setError(res.error)
      } else {
        setContent(res.content)
        setStatus(res.status)
      }
    } catch (err) {
      setError("Failed to load document")
    }
  }

  const handleSave = async () => {
    try {
      setIsSaving(true)
      await api.uploadDocument(id, content)
      await fetchDocuments()
      await loadDocument()
    } catch (err) {
      setError("Save failed")
    } finally {
      setIsSaving(false)
    }
  }

  const handleRestore = async () => {
    try {
      setIsRestoring(true)
      await api.recoverDocument(id)
      await fetchDocuments()
      await loadDocument()
    } catch (err) {
      setError("Recovery failed")
    } finally {
      setIsRestoring(false)
    }
  }

  if (!doc) {
    return <div className="status-msg error">Document not found</div>
  }

  const isCompromised = status === "compromised"

  return (
    <div>

      <button
        onClick={() => navigate("/")}
        className="secondary-btn mb-6"
      >
        ← Back to Records
      </button>

      <h1 className="section-header mb-2 !text-2xl">{doc.name}</h1>
      <p className="section-subtitle mb-6 text-sm">
        {doc.department} • Last modified: {doc.lastModified}
      </p>

      <div className="section-card overflow-hidden">

        <div className="flex justify-between border-b border-slate-200 bg-slate-50 px-6 py-4">
          <h2 className="font-semibold">DOCUMENT CONTENT</h2>

          <button
            onClick={handleSave}
            disabled={isSaving}
            className="primary-btn !py-2 !text-sm disabled:opacity-60"
          >
            {isSaving ? "Saving..." : "Save Changes"}
          </button>
        </div>

        <div className="p-6">
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="h-96 w-full rounded-lg border border-slate-200 bg-slate-50 p-4 font-mono text-sm outline-none focus:border-blue-500 focus:bg-white"
          />
        </div>

      </div>

      <div className={`mt-6 p-4 rounded border ${
        isCompromised
          ? "bg-red-50 border-red-200"
          : "bg-emerald-50 border-emerald-200"
      }`}>
        <h3 className="font-semibold mb-2">Integrity Status</h3>
        <p className="text-sm">
          {isCompromised
            ? "⚠️ Integrity check failed — Document compromised."
            : "✓ Document integrity verified."}
        </p>

        {isCompromised && (
          <button
            onClick={handleRestore}
            disabled={isRestoring}
            className="mt-3 primary-btn !bg-amber-500 hover:!bg-amber-600 disabled:opacity-60"
          >
            {isRestoring ? "Recovering..." : "Initiate Recovery"}
          </button>
        )}
      </div>

      {error && (
        <div className="status-msg error mt-4">
          {error}
        </div>
      )}

    </div>
  )
}