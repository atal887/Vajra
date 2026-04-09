import { useNavigate } from "react-router-dom"
import { useState } from "react"
import { useRecords } from "../context/RecordsContext"
import StatusBadge from "../components/StatusBadge"
import * as api from "../services/api"

export default function Records() {
    const { documents, fetchDocuments } = useRecords()
    const navigate = useNavigate()
    const visibleDocs = documents.filter(d => d.status !== "compromised")
    const [form, setForm] = useState({ id: "", name: "", department: "", content: "" })
    const [createError, setCreateError] = useState("")
    const [isCreating, setIsCreating] = useState(false)

    const activeCount = documents.filter(d => d.status === "active").length
    const compromisedCount = documents.filter(d => d.status === "compromised").length
    const recoveryCount = documents.filter(d => d.status === "recovery").length

    const handleCreateRecord = async () => {
        const id = form.id.trim()
        const name = form.name.trim()
        const department = form.department.trim()
        const content = form.content.trim()

        if (!id || !name || !department || !content) {
            setCreateError("Please fill id, name, department, and content.")
            return
        }

        try {
            setIsCreating(true)
            setCreateError("")

            const created = await api.createDocument({ id, name, department })
            if (created?.error) {
                setCreateError(created.error)
                return
            }

            const uploaded = await api.uploadDocument(id, content)
            if (uploaded?.error) {
                setCreateError(uploaded.error)
                return
            }

            setForm({ id: "", name: "", department: "", content: "" })
            await fetchDocuments()
        } catch (error) {
            setCreateError("Failed to create record.")
        } finally {
            setIsCreating(false)
        }
    }

    return (
        <div>
            <div className="mb-8">
                <h2 className="section-header">Records Dashboard</h2>
                <p className="section-subtitle">Municipal document registry - {visibleDocs.length} records on file</p>
            </div>

            <div className="section-card mb-8 p-6">
                <h3 className="mb-4 text-lg font-semibold text-slate-900">Add Record</h3>
                <div className="grid gap-3 md:grid-cols-3">
                    <input
                        value={form.id}
                        onChange={(e) => setForm(prev => ({ ...prev, id: e.target.value }))}
                        placeholder="Record ID"
                        className="rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-blue-500"
                    />
                    <input
                        value={form.name}
                        onChange={(e) => setForm(prev => ({ ...prev, name: e.target.value }))}
                        placeholder="Document Name"
                        className="rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-blue-500"
                    />
                    <input
                        value={form.department}
                        onChange={(e) => setForm(prev => ({ ...prev, department: e.target.value }))}
                        placeholder="Department"
                        className="rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-blue-500"
                    />
                </div>
                <textarea
                    value={form.content}
                    onChange={(e) => setForm(prev => ({ ...prev, content: e.target.value }))}
                    placeholder="Document content"
                    className="mt-3 h-28 w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-blue-500"
                />
                <div className="mt-3 flex items-center gap-3">
                    <button onClick={handleCreateRecord} className="primary-btn" disabled={isCreating}>
                        {isCreating ? "Adding..." : "Add Record"}
                    </button>
                    {createError && <span className="text-sm text-red-600">{createError}</span>}
                </div>
            </div>

            {/* Stats */}
            <div className="mb-8 grid gap-4 md:grid-cols-3">
                <StatCard title="Active Records" value={activeCount} color="text-green-600" />
                <StatCard title="Integrity Alerts" value={compromisedCount} color="text-red-600" />
                <StatCard title="Under Recovery" value={recoveryCount} color="text-yellow-600" />
            </div>

            {/* Table */}
            <div className="section-card overflow-hidden">
                <div className="border-b border-slate-200 bg-slate-50 px-6 py-4">
                    <h2 className="font-semibold text-slate-900">Official Documents</h2>
                </div>

                <div className="overflow-x-auto">
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>Document Name</th>
                            <th>Department</th>
                            <th>Status</th>
                            <th>Last Modified</th>
                            <th>Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        {visibleDocs.map(doc => (
                            <tr key={doc.id}>
                                <td className="font-medium text-slate-900 flex items-center gap-2">
                                    <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 8V6a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H8a2 2 0 01-2-2v-2" /><path strokeLinecap="round" strokeLinejoin="round" d="M6 12h6" /></svg>
                                    {doc.name}
                                </td>

                                <td className="text-slate-600">
                                    {doc.department}
                                </td>

                                <td>
                                    <StatusBadge status={doc.status} />
                                </td>

                                <td className="text-slate-600">
                                    {doc.lastModified}
                                </td>

                                <td className="whitespace-nowrap">
                                    <button
                                        onClick={() => navigate(`/document/${doc.id}`)}
                                        className="secondary-btn mr-2 !px-3 !py-1.5 !text-xs"
                                    >
                                        <svg className="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                        </svg>
                                        Open
                                    </button>
                                    <button
                                        onClick={async () => {
                                            await api.deleteDocument(doc.id)
                                            window.location.reload()
                                        }}
                                        className="danger-btn !px-3 !py-1.5 !text-xs"
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                </div>
            </div>
        </div>
    )
}

function StatCard({ title, value, color }) {
    return (
        <div className="section-card p-6">
            <div className={`text-3xl font-semibold ${color} mb-1`}>
                {value}
            </div>
            <div className="text-sm text-slate-500">
                {title}
            </div>
        </div>
    )
}