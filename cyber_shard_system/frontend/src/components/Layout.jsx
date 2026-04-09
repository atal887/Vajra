import Sidebar from "./Sidebar"

export default function Layout({ children }) {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand">
          MCD Internal
          <span className="brand-tag">Secure Access Lvl 01</span>
        </div>
        <div className="text-sm text-slate-500">Production Registry</div>
      </header>

      <div className="layout-main">
        <Sidebar />
        <main className="main-content">{children}</main>
      </div>
    </div>
  )
}
