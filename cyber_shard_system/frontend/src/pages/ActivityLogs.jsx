import { useState } from "react"

export default function ActivityLogs() {
  const [logs] = useState([
    { id: 1, timestamp: "2026-02-24 16:32:14", action: "Document Access", user: "Admin", details: "Municipal Budget Ordinance FY2026 opened", status: "success" },
    { id: 2, timestamp: "2026-02-24 15:45:22", action: "Integrity Check", user: "System", details: "All shards verified successfully", status: "success" },
    { id: 3, timestamp: "2026-02-24 14:12:08", action: "Document Upload", user: "Records Officer", details: "Zoning Amendment Resolution uploaded", status: "success" },
    { id: 4, timestamp: "2026-02-24 13:28:45", action: "Recovery Operation", user: "Security Team", details: "Parity chunk used to restore shard", status: "warning" },
    { id: 5, timestamp: "2026-02-24 12:15:33", action: "System Sync", user: "System", details: "Distributed nodes synchronized", status: "success" },
    { id: 6, timestamp: "2026-02-24 11:02:10", action: "Access Denied", user: "Unauthorized", details: "Attempted unauthorized document access", status: "error" }
  ])

  return (
    <div>
      <div className="mb-8">
        <div>
          <h1 className="section-header">Activity Logs</h1>
          <p className="section-subtitle">Complete audit trail of system operations and document access</p>
        </div>
      </div>

      <div className="section-card overflow-hidden">
        <div className="overflow-x-auto">
        <table className="data-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Action</th>
              <th>User</th>
              <th>Details</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {logs.map(log => (
              <tr key={log.id}>
                <td className="font-mono text-xs text-slate-600">{log.timestamp}</td>
                <td className="font-medium text-slate-900">{log.action}</td>
                <td className="text-slate-600">{log.user}</td>
                <td className="text-slate-700">{log.details}</td>
                <td>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    log.status === "success"
                      ? "bg-emerald-50 text-emerald-700"
                      : log.status === "warning"
                      ? "bg-amber-50 text-amber-700"
                      : "bg-red-50 text-red-700"
                  }`}>
                    {log.status.charAt(0).toUpperCase() + log.status.slice(1)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        </div>
      </div>

      <div className="mt-4 flex items-center justify-between">
        <div className="text-sm text-slate-600">
          Showing 1 to 6 of 2,341 logs
        </div>
        <div className="flex gap-2">
          <button className="secondary-btn !px-4 !py-2">Previous</button>
          <button className="primary-btn !px-4 !py-2">1</button>
          <button className="secondary-btn !px-4 !py-2">2</button>
          <button className="secondary-btn !px-4 !py-2">3</button>
          <button className="secondary-btn !px-4 !py-2">Next</button>
        </div>
      </div>
    </div>
  )
}
