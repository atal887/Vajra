import os
import time
import sqlite3
import numpy as np
import cv2
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from contextlib import asynccontextmanager

# Forensic Logic & DB Init
from logic import get_dna_hash, stamp_image, get_document_dna
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Boot sequence to ensure forensic folders and DB schema are ready."""
    for folder in ["captured_images", "captured_documents", "templates", "static"]:
        os.makedirs(folder, exist_ok=True)
    init_db() 
    yield

app = FastAPI(lifespan=lifespan)

# SAFARI FIX: Use absolute path for static mounting to prevent 404/Security errors
static_abs_path = os.path.join(os.getcwd(), "static")
app.mount("/static", StaticFiles(directory=static_abs_path), name="static")

templates = Jinja2Templates(directory="templates")

def get_db():
    conn = sqlite3.connect('mcd_records.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- INITIAL REGISTRATION ---
@app.post("/upload-image")
async def upload_image(officer_id: str = Form(...), status: str = Form(...), file: UploadFile = File(...)):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    contents = await file.read()
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    
    # Generate and hide forensic DNA in pixels
    dna = get_dna_hash(officer_id, status, ts)
    path = f"captured_images/{officer_id}_{int(time.time())}.png"
    cv2.imwrite(path, stamp_image(img, dna))
    
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO reports (officer_id, status, timestamp, dna_hash, image_path) VALUES (?,?,?,?,?)", 
                 (officer_id, status, ts, dna, path))
    # Truth source for the Shadow Vault
    conn.execute("INSERT OR REPLACE INTO shadow_logs (officer_id, original_status) VALUES (?,?)", 
                 (officer_id, status))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.post("/upload-doc")
async def upload_document(officer_id: str = Form(...), doc_name: str = Form(...), file: UploadFile = File(...)):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = f"captured_documents/{int(time.time())}_{file.filename}"
    with open(path, "wb") as f: f.write(await file.read())
        
    dna = get_document_dna(path)
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO document_vault (officer_id, doc_name, doc_type, timestamp, file_dna, file_path) VALUES (?,?,'DOC',?,?,?)", 
                 (officer_id, doc_name, ts, dna, path))
    conn.execute("INSERT OR REPLACE INTO shadow_logs (officer_id, original_status) VALUES (?,?)", 
                 (officer_id, f"DOC:{doc_name}"))
    conn.commit()
    conn.close()
    return {"status": "success"}

# --- MULTI-ALERT AUDIT ENGINE ---
@app.get("/api/audit-check")
async def audit_system():
    """Deep Forensic Audit: Scans the entire registry for multiple hacks."""
    conn = get_db()
    alerts = []
    try:
        # 1. Metadata Check (Database Hijacking)
        db_mismatches = conn.execute("""
            SELECT r.officer_id, r.status, s.original_status 
            FROM reports r 
            JOIN shadow_logs s ON r.officer_id = s.officer_id 
            WHERE r.status != s.original_status
        """).fetchall()
        for m in db_mismatches:
            alerts.append({"id": m[0], "type": "DATABASE", "new": m[1], "ts": datetime.now().strftime("%H:%M:%S")})

        # 2. Pixel DNA Check (Image Tampering)
        imgs = conn.execute("SELECT officer_id, dna_hash, image_path FROM reports").fetchall()
        for i in imgs:
            if os.path.exists(i['image_path']):
                img_data = cv2.imread(i['image_path'])
                if img_data is not None:
                    flat_img = img_data.flatten()
                    # Extract 512 bits to verify DNA signature
                    extracted_bits = "".join([str(flat_img[j] & 1) for j in range(512)])
                    extracted_dna = "".join([chr(int(extracted_bits[j:j+8], 2)) for j in range(0, 512, 8)]).strip()
                    if extracted_dna != i['dna_hash']:
                        alerts.append({"id": i['officer_id'], "type": "IMAGE_PIXELS", "ts": datetime.now().strftime("%H:%M:%S")})

        # 3. Binary Check (Document Tampering)
        docs = conn.execute("SELECT officer_id, file_dna, file_path FROM document_vault").fetchall()
        for d in docs:
            if os.path.exists(d['file_path']) and get_document_dna(d['file_path']) != d['file_dna']:
                alerts.append({"id": d['officer_id'], "type": "BINARY", "ts": datetime.now().strftime("%H:%M:%S")})
                
    except Exception as e: print(f"Audit Error: {e}")
    conn.close()
    return {"tampered": len(alerts) > 0, "alerts": alerts}

@app.get("/api/assets")
async def get_assets():
    conn = get_db()
    imgs = conn.execute("SELECT officer_id as id, 'IMAGE' as type, status as info, timestamp FROM reports").fetchall()
    docs = conn.execute("SELECT officer_id as id, 'DOCUMENT' as type, doc_name as info, timestamp FROM document_vault").fetchall()
    res = [dict(r) for r in imgs] + [dict(r) for r in docs]
    conn.close()
    return res

# --- RESTORATION LOGIC ---

@app.post("/api/repair")
async def repair_data(officer_id: str = Form(...)):
    """10-second Shadow Vault restoration."""
    time.sleep(10) 
    conn = get_db()
    truth = conn.execute("SELECT original_status FROM shadow_logs WHERE officer_id = ?", (officer_id,)).fetchone()
    if truth:
        conn.execute("UPDATE reports SET status = ? WHERE officer_id = ?", (truth[0], officer_id))
        conn.commit()
    conn.close()
    return {"status": "RESTORED"}

@app.post("/api/reupload")
async def resecure_asset(
    officer_id: str = Form(...), # Previous Key
    new_id: str = Form(...),     # Verified Key
    new_status: str = Form(...), # Verified Metadata
    type: str = Form(...), 
    file: UploadFile = File(...)
):
    """Full forensic restoration: Re-stamps DNA into pixels to fix the Red Alert."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    contents = await file.read()
    conn = get_db()
    
    if type == 'IMAGE':
        img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
        dna = get_dna_hash(new_id, new_status, ts)
        path = f"captured_images/resecured_{int(time.time())}.png"
        cv2.imwrite(path, stamp_image(img, dna)) # RE-STAMPING
        
        conn.execute("UPDATE reports SET officer_id=?, status=?, dna_hash=?, image_path=?, timestamp=? WHERE officer_id=?", 
                     (new_id, new_status, dna, path, ts, officer_id))
    else:
        path = f"captured_documents/resecured_{int(time.time())}_{file.filename}"
        with open(path, "wb") as f: f.write(contents)
        dna = get_document_dna(path)
        conn.execute("UPDATE document_vault SET officer_id=?, doc_name=?, file_dna=?, file_path=?, timestamp=? WHERE officer_id=?", 
                     (new_id, new_status, dna, path, ts, officer_id))
    
    # Sync Shadow Vault
    conn.execute("UPDATE shadow_logs SET officer_id=?, original_status=? WHERE officer_id=?", 
                 (new_id, new_status, officer_id))
    conn.commit()
    conn.close()
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)