# 🛡️ Vajra – Multi-Layer Cybersecurity Defense System

## 🚀 Overview

**Vajra** is a full-stack cybersecurity platform designed to simulate and demonstrate a **multi-layer defense architecture**. It combines distributed storage, intrusion detection, and system-level defense mechanisms into one unified system.

This project showcases concepts from:

* Cybersecurity
* Distributed Systems
* Backend + Frontend Integration
* Systems Programming (C++)

---

## 🧩 Core Modules

### 🔐 Cyber Shard System

* Secure distributed data storage using sharding
* Data split across multiple storage servers
* Reduces risk of single-point data breaches

### 📊 MCD (Monitoring & Cyber Detection)

* Detects suspicious activities
* Simulates cyber attacks (documents, images, etc.)
* Generates alerts and logs

### ⚔️ MCD Defense

* High-performance backend built in C++
* Handles secure communication and request validation
* Strengthens system against malicious inputs

### 🌐 Vajra MCD (Web Layer)

* Web-based interface for system interaction
* Configurable server setup (NGINX/OpenResty based)
* Acts as control panel for monitoring + defense

---

## 🏗️ System Architecture

```
User Request
     ↓
Frontend (React / Web UI)
     ↓
Backend (Python APIs)
     ↓
Data Sharding Layer
     ↓
Storage Servers (Distributed)
     ↓
Detection Layer (MCD)
     ↓
Defense Layer (C++)
```

---

## ⚙️ Tech Stack

* **Frontend:** React, HTML, CSS, Vite
* **Backend:** Python (Flask/FastAPI style APIs)
* **Systems Layer:** C++
* **Security Concepts:** Encryption, Sharding, Intrusion Detection
* **Web Server:** NGINX / OpenResty (config-based)

---

## 📁 Project Structure

```
final_project/
│
├── cyber_shard_system/   # Distributed storage + frontend
├── MCD/                  # Detection & monitoring system
├── MCD_defense/          # C++ defense backend
├── vajra-mcd/            # Web + config layer
├── command.txt           # Utility commands
└── .gitignore
```

---

## ▶️ How to Run

### 1. Clone the Repository

```
git clone https://github.com/your-username/Vajra.git
cd Vajra
```

---

### 2. Run Cyber Shard Backend

```
cd cyber_shard_system/backend
pip install -r requirements.txt
python main_server.py
```

---

### 3. Run Storage Servers

```
cd storage_server1
python server.py
```

Repeat for server2 and server3.

---

### 4. Run Frontend

```
cd cyber_shard_system/frontend
npm install
npm run dev
```

---

### 5. Run MCD System

```
cd MCD
python server.py
```

---

### 6. Run MCD Defense (C++)

```
cd MCD_defense/backend
g++ main.cpp -o server
./server
```

---

## ⚠️ Important Notes

* Large datasets, logs, and binaries are **excluded** from this repository.
* External dependencies (like OpenSSL/OpenResty) must be installed separately.
* This project is intended for **educational and demonstration purposes**.

---

## 🎯 Key Highlights

* Multi-layer security architecture
* Combines Python, C++, and React in one system
* Demonstrates real-world cybersecurity concepts
* Modular and scalable design
* Plug and Protect Integration

---

## 📌 Future Improvements

* Real-time attack visualization dashboard
* Cloud deployment (AWS/GCP)
* Authentication & role-based access
* Advanced threat detection using ML

---
