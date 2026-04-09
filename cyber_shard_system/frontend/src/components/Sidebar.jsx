
import { Link, useLocation } from "react-router-dom"

function SidebarIcon({ type }) {
    switch (type) {
        case "records":
            return (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 8V6a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H8a2 2 0 01-2-2v-2" /><path strokeLinecap="round" strokeLinejoin="round" d="M6 12h6" /></svg>
            )
        case "security":
            return (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 3l8 4v5c0 5.25-3.5 10-8 12-4.5-2-8-6.75-8-12V7l8-4z" /></svg>
            )
        case "logs":
            return (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 10h16M4 14h16M4 18h16" /></svg>
            )
        default:
            return null
    }
}

export default function Sidebar() {
    const location = useLocation()
    const navItems = [
        { path: "/", label: "Records", icon: "records" },
        { path: "/security", label: "Security Console", icon: "security" },
        { path: "/logs", label: "Activity Logs", icon: "logs" }
    ]

    return (
        <aside className="w-full border-b border-slate-200 bg-white p-4 md:w-64 md:border-b-0 md:border-r md:p-6">
            <div className="mb-5">
                <div className="flex items-center gap-3">
                    <div className="h-9 w-9 rounded-md bg-blue-600 text-base font-bold text-white flex items-center justify-center">M</div>
                    <div>
                        <div className="text-sm font-semibold tracking-tight text-slate-900">Municipal Records</div>
                        <div className="text-xs text-slate-500">Management Console</div>
                    </div>
                </div>
            </div>

            <nav className="space-y-1">
                {navItems.map(item => (
                    <Link
                        key={item.path}
                        to={item.path}
                        className={`flex items-center gap-3 rounded-lg border px-4 py-2.5 text-sm font-medium transition ${location.pathname === item.path
                                ? "border-blue-200 bg-blue-50 text-blue-700"
                                : "border-transparent text-slate-600 hover:border-slate-200 hover:bg-slate-50 hover:text-slate-900"
                            }`}
                    >
                        <SidebarIcon type={item.icon} />
                        <span>{item.label}</span>
                    </Link>
                ))}
            </nav>

            <div className="mt-6 border-t border-slate-200 pt-4 text-xs text-slate-500">
                <div className="font-semibold text-emerald-600">System Status: Operational</div>
                <div>v3.2.1 • TLS 1.3 Secured</div>
            </div>
        </aside>
    )
}
