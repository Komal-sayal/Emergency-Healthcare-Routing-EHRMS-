import React, { useState } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import VoiceButton from './components/VoiceButton'
import Dashboard from './pages/Dashboard'
import HospitalDirectory from './pages/HospitalDirectory'
import EmergencyRouter from './pages/EmergencyRouter'
import AmbulanceTracker from './pages/AmbulanceTracker'
import BudgetFinder from './pages/BudgetFinder'
import EmergencyLog from './pages/EmergencyLog'
import HospitalDetail from './pages/HospitalDetail'
import NotFound from './pages/NotFound'
import VoiceAction from './pages/VoiceAction'
import VoiceSetup from './pages/VoiceSetup'
import RoleSelect from './pages/RoleSelect'
import HospitalCommand from './pages/HospitalCommand'
import './styles/globals.css'

function AppLayout({ activePage, setActivePage, children }) {
  return (
    <div className="app-root">
      <Sidebar activePage={activePage} setActivePage={setActivePage} />
      <div className="main-wrap">
        <Topbar activePage={activePage} />
        <div className="page-content">{children}</div>
      </div>
      <VoiceButton />
    </div>
  )
}

export default function App() {
  const [activePage, setActivePage] = useState('dashboard')

  const wrap = (Component) => (
    <AppLayout activePage={activePage} setActivePage={setActivePage}>
      <Component setActivePage={setActivePage} />
    </AppLayout>
  )

  return (
    <Routes>
      {/* Entry point — role selection */}
      <Route path="/"                 element={<RoleSelect />} />

      {/* Hospital staff portal */}
      <Route path="/hospital-command" element={<HospitalCommand />} />

      {/* Patient / public app */}
      <Route path="/dashboard"        element={wrap(Dashboard)} />
      <Route path="/hospitals"        element={wrap(HospitalDirectory)} />
      <Route path="/hospitals/:id"    element={
        <AppLayout activePage={activePage} setActivePage={setActivePage}>
          <HospitalDetail />
        </AppLayout>
      } />
      <Route path="/emergency-router" element={wrap(EmergencyRouter)} />
      <Route path="/ambulances"       element={wrap(AmbulanceTracker)} />
      <Route path="/budget"           element={wrap(BudgetFinder)} />
      <Route path="/emergency-log"    element={wrap(EmergencyLog)} />
      <Route path="/voice-setup"      element={wrap(VoiceSetup)} />
      <Route path="/voice"            element={<VoiceAction />} />
      <Route path="*"                 element={<NotFound />} />
    </Routes>
  )
}
