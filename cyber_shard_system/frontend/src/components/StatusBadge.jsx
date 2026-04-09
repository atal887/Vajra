export default function StatusBadge({ status }) {
  const statusConfig = {
    active: { bg: "bg-emerald-50", text: "text-emerald-700", label: "Active" },
    compromised: { bg: "bg-red-50", text: "text-red-700", label: "Integrity Alert" },
    recovery: { bg: "bg-amber-50", text: "text-amber-700", label: "Under Recovery" },
  }

  const config = statusConfig[status] || statusConfig.active

  return (
    <span className={`inline-flex items-center rounded-md px-2.5 py-1 text-xs font-semibold ${config.bg} ${config.text}`}>
      {config.label}
    </span>
  )
}