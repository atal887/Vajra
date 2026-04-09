// import React, { createContext, useContext, useState, useCallback } from "react"
// import * as api from "../services/api"

// const RecordsContext = createContext()

// function simpleHash(str) {
//   let hash = 0
//   for (let i = 0; i < str.length; i++) {
//     const char = str.charCodeAt(i)
//     hash = ((hash << 5) - hash) + char
//     hash |= 0
//   }
//   return Math.abs(hash).toString(16).padStart(8, "0").toUpperCase()
// }

// const initialDocuments = [
//   {
//     id: "doc1",
//     name: "Municipal Budget Ordinance FY2026",
//     department: "Finance",
//     status: "active",
//     lastModified: "2026-02-24 16:32",
//     originalContent: `MUNICIPAL BUDGET ORDINANCE — FISCAL YEAR 2026

// Section 1. Short Title
// This ordinance shall be known as the "Annual Budget Ordinance for Fiscal Year 2026."

// Section 2. Appropriations
// The following sums are hereby appropriated for the fiscal year beginning July 1, 2025:

//   General Fund Operations: $24,500,000
//   Public Safety: $8,200,000
//   Infrastructure Maintenance: $5,750,000
//   Parks & Recreation: $2,100,000
//   Administrative Services: $3,450,000

// Section 3. Revenue Estimates
// Total estimated revenue for FY2026: $44,000,000

// Section 4. Effective Date
// This ordinance takes effect upon adoption by the Municipal Council.`,
//     currentContent: "",
//     originalHash: "",
//     currentHash: "",
//   },
//   {
//     id: "doc2",
//     name: "Zoning Amendment Resolution 2026-03",
//     department: "Urban Planning",
//     status: "active",
//     lastModified: "2026-02-18 09:15",
//     originalContent: `RESOLUTION NO. 2026-03
// AMENDMENT TO MUNICIPAL ZONING CODE

// WHEREAS, the Municipal Planning Commission has reviewed the current zoning designations for District 7; and

// WHEREAS, the proposed changes will support sustainable development goals;

// NOW, THEREFORE, BE IT RESOLVED:

// Section 1. The zoning classification for parcels 7-101 through 7-115 is hereby changed from R-1 (Residential) to MU-2 (Mixed Use).

// Section 2. All development within the reclassified area shall comply with the Mixed Use Design Standards.

// Section 3. This resolution shall take effect 30 days after adoption.`,
//     currentContent: "",
//     originalHash: "",
//     currentHash: "",
//   },
//   {
//     id: "doc3",
//     name: "Public Works Contract #PW-2026-017",
//     department: "Public Works",
//     status: "active",
//     lastModified: "2026-02-22 11:45",
//     originalContent: `CONTRACT FOR MUNICIPAL ROAD REHABILITATION
// Contract No: PW-2026-017

// Parties:
//   Municipality of Greenfield
//   Contractor: Atlas Infrastructure Corp.

// Scope of Work:
//   Rehabilitation of Main Street from 1st Avenue to 12th Avenue
//   Total length: 2.4 miles
//   Includes: resurfacing, drainage improvements, ADA curb ramps

// Contract Amount: $3,275,000
// Commencement Date: March 15, 2026
// Completion Date: September 30, 2026

// Performance Bond: 100% of contract amount
// Payment Terms: Monthly progress payments, 10% retainage`,
//     currentContent: "",
//     originalHash: "",
//     currentHash: "",
//   },
//   {
//     id: "doc4",
//     name: "Emergency Services Mutual Aid Agreement",
//     department: "Public Safety",
//     status: "active",
//     lastModified: "2026-02-15 16:20",
//     originalContent: `MUTUAL AID AGREEMENT
// BETWEEN GREENFIELD MUNICIPALITY AND NEIGHBORING JURISDICTIONS

// This agreement establishes mutual aid provisions for emergency response services.

// Participating Jurisdictions:
//   City of Greenfield
//   Township of Oakdale
//   Borough of Riverside

// Services Covered:
//   Fire suppression and rescue
//   Emergency medical services
//   Hazardous materials response
//   Search and rescue operations

// Activation: Upon request by any participating jurisdiction's Emergency Management Coordinator.

// Cost Sharing: Each jurisdiction bears its own costs for the first 24 hours. Extended deployments subject to reimbursement.`,
//     currentContent: "",
//     originalHash: "",
//     currentHash: "",
//   },
//   {
//     id: "doc5",
//     name: "Water Quality Compliance Report Q1-2026",
//     department: "Environmental Services",
//     status: "active",
//     lastModified: "2026-02-24 08:00",
//     originalContent: `QUARTERLY WATER QUALITY COMPLIANCE REPORT
// Period: January 1 — March 31, 2026
// Facility: Greenfield Municipal Water Treatment Plant

// Compliance Summary:
//   All parameters within EPA and state regulatory limits
//   Zero violations reported

// Key Metrics:
//   Turbidity: 0.12 NTU (limit: 1.0 NTU)
//   Chlorine Residual: 0.8 mg/L (range: 0.2–4.0 mg/L)
//   Lead: <1 ppb (action level: 15 ppb)
//   Coliform: 0 positive samples

// Certified by: Dr. Sarah Chen, Water Quality Director`,
//     currentContent: "",
//     originalHash: "",
//     currentHash: "",
//   },
// ]

// // Initialize hashes
// initialDocuments.forEach((doc) => {
//   doc.originalHash = simpleHash(doc.originalContent)
//   doc.currentHash = doc.originalHash
//   doc.currentContent = doc.originalContent
// })

// export function RecordsProvider({ children }) {
//   const [documents, setDocuments] = useState(initialDocuments)

//   // Seed backend on mount
//   React.useEffect(() => {
//     try {
//       api.seedDocuments(initialDocuments.map(d => ({ id: d.id, name: d.name, department: d.department })))
//     } catch (err) {
//       console.error("Failed to seed backend:", err)
//     }
//   }, [])

//   const updateDocument = useCallback((id, newContent) => {
//     setDocuments((prev) =>
//       prev.map((doc) => {
//         if (doc.id !== id) return doc
//         const newHash = simpleHash(newContent)
//         const isCompromised = newHash !== doc.originalHash
//         return {
//           ...doc,
//           currentContent: newContent,
//           currentHash: newHash,
//           status: isCompromised ? "compromised" : "active",
//           lastModified: new Date().toLocaleString("sv-SE").replace("T", " ").slice(0, 16),
//         }
//       })
//     )
//   }, [])

//   const restoreDocument = useCallback((id) => {
//     setDocuments((prev) =>
//       prev.map((doc) => {
//         if (doc.id !== id) return doc
//         return {
//           ...doc,
//           currentContent: doc.originalContent,
//           currentHash: doc.originalHash,
//           status: "active",
//           lastModified: new Date().toLocaleString("sv-SE").replace("T", " ").slice(0, 16),
//         }
//       })
//     )
//   }, [])

//   const getDocument = useCallback(
//     (id) => documents.find((d) => d.id === id),
//     [documents]
//   )

//   return (
//     <RecordsContext.Provider value={{ documents, updateDocument, restoreDocument, getDocument }}>
//       {children}
//     </RecordsContext.Provider>
//   )
// }

// export const useRecords = () => {
//   const ctx = useContext(RecordsContext)
//   if (!ctx) throw new Error("useRecords must be used within RecordsProvider")
//   return ctx
// }

import React, { createContext, useContext, useState, useEffect, useCallback } from "react"
import * as api from "../services/api"

const RecordsContext = createContext()

export function RecordsProvider({ children }) {
  const [documents, setDocuments] = useState([])

  const fetchDocuments = useCallback(async () => {
    try {
      const data = await api.getDocuments()
      setDocuments(data)
    } catch (err) {
      console.error("Failed to fetch documents:", err)
    }
  }, [])

  useEffect(() => {
    fetchDocuments()
  }, [fetchDocuments])

  useEffect(() => {
  const interval = setInterval(fetchDocuments, 5000)
  return () => clearInterval(interval)
}, [fetchDocuments])

  const updateDocument = useCallback(async (id, newContent) => {
    try {
      await api.uploadDocument(id, newContent)
      await fetchDocuments()
    } catch (err) {
      console.error("Update failed:", err)
    }
  }, [fetchDocuments])

  const restoreDocument = useCallback(async (id) => {
    try {
      await api.recoverDocument(id)
      await fetchDocuments()
    } catch (err) {
      console.error("Recovery failed:", err)
    }
  }, [fetchDocuments])

  const getDocument = useCallback(
    (id) => documents.find((d) => d.id === id),
    [documents]
  )

  return (
    <RecordsContext.Provider value={{ 
  documents, 
  updateDocument, 
  restoreDocument, 
  getDocument,
  fetchDocuments
}}>
      {children}
    </RecordsContext.Provider>
  )
}

export const useRecords = () => {
  const ctx = useContext(RecordsContext)
  if (!ctx) throw new Error("useRecords must be used within RecordsProvider")
  return ctx
}