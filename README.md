# Vajra: Multi-Layer Cybersecurity Defense System

Vajra provides advanced cybersecurity through distributed sharding, intrusion detection, and multi-layer defense.

## Team Members

- Nandini Atal  
- Navya Jindal  
- Aryan Bansal  
- Mehak Taneja  


---

### Tech Stack

![Python](https://img.shields.io/badge/Python-3.x-blue)
![C++](https://img.shields.io/badge/C++-blue)
![React](https://img.shields.io/badge/React-Frontend-blue)
![NGINX](https://img.shields.io/badge/NGINX-Server-green)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-UI-blue)
![Gemini API](https://img.shields.io/badge/Gemini-API-orange)

---

## Important

<p align="center"><strong>Demo Video</strong></p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=VIDEO_ID">
    <img src="https://img.youtube.com/vi/VIDEO_ID/0.jpg" width="700">
  </a>
</p>

<p align="center"><strong>Play Demo on YouTube</strong></p>

## Table of Contents
 [1. Overview](#1-overview)  
 [2. Why This Project Stands Out](#2-why-this-project-stands-out)  
 [3. Architecture](#3-architecture)  
 [4. Features](#4-features)  
 [5. Layer 1: Fake Database Layer](#5-layer-1-fake-database-layer)  
 [6. Layer 2: Resource Tarpit](#6-layer-2-resource-tarpit)  
 [7. Layer 3: Chronos Locks](#7-layer-3-chronos-locks)  
 [8. Layer 4: Botnet Math Layer](#8-layer-4-botnet-math-layer)  
 [9. Layer 5: Bit-Level Fragmentation](#9-layer-5-bit-level-fragmentation)  
 [10. Project Structure](#10-project-structure)  
 [11. Install and Run](#11-install-and-run)  
 [12. Usage Examples](#12-usage-examples)  
 [13. Tech Stack](#13-tech-stack)  
 [14. Testing](#14-testing)  
 [15. Visual Showcase](#15-visual-showcase)  
 [16. Team and Credits](#16-team-and-credits)  
 [17. Future Improvements](#17-future-improvements)  

## 1. Overview

Vajra offers 5-layer architecture to protect startups and SMEs against hackers. Startups lack resources for expensive security, so Vajra is cost-effective. It defends against advanced attacks like LLM-based botnets—protection not available in AWS or other cloud systems.

**USP: Plug and Protect Integration**  
Startups provide DB URL; Vajra acts as proxy layer, generates secure URL. No direct use of startup DB—we fully isolate it for fault-safe operation.

**5-Layer Architecture:**
1. **Fake DB Layer**: Decoy database with honeypot data to trap attackers.  
2. **Resource Tarpit**: Slows attackers by serving heavy dummy computations.  
3. **Chronos Locks**: Time-based locks delay requests, preventing rapid attacks.  
4. **Botnet Math Layer**: Math challenges (PoW) block botnets/LLM attacks.  
5. **Bit-Level Fragmentation**: Data sharded at bit level across nodes, impossible to reconstruct without all fragments.

## 2. Why This Project Stands Out

- Cost-effective protection for resource-constrained startups/SMEs  
- Defends advanced LLM-botnet attacks unavailable in cloud services  
- Plug-and-protect proxy—no DB changes needed  
- Fault-safe isolation of production data  
- Scalable 5-layer defense  

## 3. Architecture


![Architecture Diagram](architecture.png)
**Arrow Diagram**:
```
User Request
     ↓
Fake DB Layer
     ↓
Resource Tarpit
     ↓
Chronos Locks
     ↓
Botnet Math
     ↓
Bit-Level Fragmentation
     ↓
Secure Storage
```

## 4. Features

- Multi-layered defense architecture protecting against modern cyber threats  
- Proxy-based secure access with controlled exposure of endpoints  
- Real-time attack monitoring and logging  
- Intelligent attacker profiling and fingerprinting  
- Adaptive response system based on threat level  
- Distributed storage for enhanced data security  
- Bot and automation detection using behavioral analysis  
- Post-quantum cryptographic support for future-proof security  
- Scalable and containerized deployment using Docker  
- AI-assisted attack analysis and reporting  

**Plug and Protect**:  
Operates in a proxy mode where all incoming traffic is routed through a secure intermediary. It generates sanitized and controlled URLs, ensuring that backend services are never directly exposed. This helps in preventing direct attacks while enabling safe interaction and monitoring.

---

## 5. Layer 1: Fake Database Layer

This layer acts as the first line of deception. Instead of exposing real data, the system presents a highly realistic fake database environment designed to mislead attackers.

- Serves dynamically generated dummy data that mimics real systems  
- Protects against SQL Injection using parameterized queries and firewall rules  
- Prevents XSS attacks through strict content sanitization and security policies  
- Redirects suspicious requests into a controlled “data maze”  
- Logs attacker queries, payloads, and behavior for analysis  
- Generates forensic reports based on attacker interaction  

**Outcome**: Attacker is deceived, monitored, and isolated without accessing real data.

---

## 6. Layer 2: Resource Tarpit

This layer slows down attackers by trapping them in computationally expensive and time-consuming processes.

- Engages attackers with fake heavy workloads (encryption loops, math problems)  
- Dynamically adjusts delay intensity based on threat level  
- Prevents rapid scanning and brute-force attempts  
- Uses fingerprinting to track repeat attackers across sessions  
- Ensures minimal impact on legitimate users while isolating malicious traffic  

**Outcome**: Attacker’s time and computational resources are wasted, reducing attack efficiency.

---

## 7. Layer 3: Chronos Locks

Chronos Locks introduce time-based restrictions to limit repeated malicious attempts.

- Applies exponential delays on repeated requests  
- Detects abnormal speed patterns (e.g., impossible human response times)  
- Flags automated tools and scripted attacks  
- Tracks IP, device fingerprints, and potential VPN/proxy usage  
- Builds a timeline of attacker activity  

**Outcome**: Prevents brute-force and rapid attacks while generating a detailed attacker profile.

---

## 8. Layer 4: Botnet Math Layer

Designed to counter botnet-driven attacks by differentiating between humans and automated systems.

- Presents adaptive computational challenges  
- Easy problems for humans, complex for bots  
- Forces bots to spend excessive time solving tasks  
- Reduces economic viability of large-scale automated attacks  
- Uses cryptographic and proof-of-work style validation  

**Outcome**: Botnets are slowed down or neutralized by computational overhead.

---

## 9. Layer 5: Bit-Level Fragmentation

This layer ensures maximum data security by distributing and obfuscating stored information.

- Splits sensitive data into tiny fragments at the bit level  
- Distributes fragments across multiple storage nodes  
- Uses a unique master key (PIN-based reconstruction logic)  
- Prevents reconstruction without full authorization  
- Ensures even partial data leaks are useless  

**Outcome**: Data remains secure and unrecoverable without the correct reconstruction key.
## 10. Project Structure

```
Vajra/
│
├── cyber_shard_system/   # Distributed storage + frontend
│   ├── backend/
│   └── frontend/
├── MCD/                  # Detection & monitoring system
├── MCD_defense/          # C++ defense backend
├── vajra-mcd/            # Web + config layer
├── command.txt           # Utility commands
└── .gitignore
```

## 11. Install and Run

### 1. Clone the Repository

```
git clone https://github.com/your-username/Vajra.git
cd Vajra
```

### 2. Run Cyber Shard Backend

```
cd cyber_shard_system/backend
pip install -r requirements.txt
python main_server.py
```

### 3. Run Storage Servers

```
cd cyber_shard_system/backend/storage_server1
python server.py
```

Repeat for storage_server2 and storage_server3.

### 4. Run Frontend

```
cd cyber_shard_system/frontend
npm install
npm run dev
```

### 5. Run MCD System

```
cd MCD
python server.py
```

### 6. Run MCD Defense (C++)

```
cd MCD_defense/backend
g++ main.cpp -o server
./server
```

## 12. Usage Examples

- Access frontend at http://localhost:5173  
- Simulate attacks: python MCD/simulate_hack.py  
- Configure proxy: Edit vajra-mcd/config/nginx.conf with DB URL  
- Monitor tarpits: Security Console tab  

## 13. Tech Stack

| Technology | Purpose |
|------------|---------|
| OpenResty (Nginx + Lua) | Tarpits & pattern analysis |
| JS Canvas Fingerprinting | Bot detection |
| PHP Forensic Dossier Engine | Fake DB honeypots |
| Python (Bit-Level Sharding) | Fragmentation layer |
| Distributed SQLite | Secure storage nodes |
| CRYSTALS-Dilithium | Post-quantum signatures |
| PoW Engine | Botnet math challenges |
| SHA-256/Blake3 | Hashing & PoW |
| Crow Framework | C++ defense server |
| Chronos-Lock | Time-based throttling |
| Docker | Deployment |
| OpenCV | Steganography detection |
| Tailwind CSS | UI |
| Gemini API | Attack analysis |

## 14. Testing

- Simulate hacks: python MCD/simulate_hack.py  
- Test tarpit: curl tarpit endpoint  
- Verify fragmentation: Check storage servers  
- Frontend tests: npm test

## 15. Visual Showcase

A glimpse into Vajra's interface and multi-layer defense system in action.

## 16. Team and Credits

**Team Members:**  
Nandini Atal  
Navya Jindal  
Aryan Bansal  
Mehak Taneja  



## 17. Future Improvements

- LLM behavioral biometrics  
- AI-driven tarpit adaptation  
- Quantum-safe key management  
- Global threat intelligence sharing  

---

