import { useState } from "react"
import { useRecords } from "../context/RecordsContext"
import * as api from "../services/api"

export default function SecurityConsole() {
  const { documents, fetchDocuments } = useRecords()
  const [recovering, setRecovering] = useState(null)
  const [error, setError] = useState(null)

  const compromisedDocs = documents.filter(d => d.status === "compromised")
  const allVerified = compromisedDocs.length === 0

  const handleRecovery = async (docId) => {
    try {
      setRecovering(docId)
      setError(null)

      // Call backend recovery
      await api.recoverDocument(docId)

      // Refresh documents from backend
      await fetchDocuments()

    } catch (err) {
      console.error("Recovery failed:", err)
      setError("Failed to recover document.")
    } finally {
      setRecovering(null)
    }
  }

  return (
    <div>

      <div className="mb-8">
        <h2 className="section-header">
          Security Console
        </h2>
        <p className="section-subtitle">
          Integrity monitoring and distributed recovery operations
        </p>
      </div>

      <div className="section-card overflow-hidden">
        <div className="border-b border-slate-200 bg-slate-50 px-6 py-4">
          <h2 className="text-sm font-medium text-slate-700">
            Compromised Documents ({compromisedDocs.length})
          </h2>
        </div>

        {allVerified ? (
          <div className="px-6 py-12 text-center">
            <div className="w-10 h-10 mx-auto mb-4 rounded-full border-2 border-emerald-500 flex items-center justify-center">
              ✓
            </div>
            <h3 className="text-sm font-medium text-slate-800 mb-1">
              All Documents Verified
            </h3>
            <p className="text-xs text-slate-500">
              No integrity issues detected across distributed nodes.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>Document</th>
                <th>Department</th>
                <th>Last Modified</th>
                <th className="text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              {compromisedDocs.map(doc => (
                <tr key={doc.id}>
                  <td>{doc.name}</td>
                  <td className="text-slate-500">{doc.department}</td>
                  <td className="text-slate-500">{doc.lastModified}</td>
                  <td className="text-right">
                    <button
                      onClick={() => handleRecovery(doc.id)}
                      disabled={recovering === doc.id}
                      className="primary-btn !px-3 !py-1.5 !text-xs disabled:opacity-60"
                    >
                      {recovering === doc.id
                        ? "Recovering..."
                        : "Initiate Recovery"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
        )}
      </div>

      {error && (
        <div className="status-msg error mt-6">
          {error}
        </div>
      )}
    </div>
  )
}