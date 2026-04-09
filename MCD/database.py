import sqlite3
import os

# Absolute path for stability on your MacBook Air
DB_PATH = os.path.join(os.path.dirname(__file__), 'mcd_records.db')

def init_db():
    """Initializes the MCD Forensic Registry with a Shadow Vault for recovery."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Main Reports Table (Image DNA)
    # Using officer_id as PRIMARY KEY ensures unique records and easier auditing
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            officer_id TEXT PRIMARY KEY, 
            status TEXT, 
            timestamp TEXT, 
            dna_hash TEXT, 
            image_path TEXT
        )
    ''')

    # 2. Document Vault Table (Binary DNA)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_vault (
            officer_id TEXT PRIMARY KEY,
            doc_name TEXT,
            doc_type TEXT,
            timestamp TEXT,
            file_dna TEXT,
            file_path TEXT
        )
    ''')
    
    # 3. Shadow Vault (Immutable Backup)
    # Stores the original 'Truth' to detect and repair database tampering
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shadow_logs (
            officer_id TEXT PRIMARY KEY, 
            original_status TEXT, 
            timestamp TEXT, 
            dna_hash TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("--- [DB] MCD Forensic Database & Shadow Vault Initialized ---")

def save_record(officer_id, status, timestamp, dna_hash, image_path):
    """Saves Image DNA and creates a Shadow Backup for recovery."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # INSERT OR REPLACE handles re-uploads or updates to the same Officer ID
        cursor.execute('''
            INSERT OR REPLACE INTO reports (officer_id, status, timestamp, dna_hash, image_path) 
            VALUES (?,?,?,?,?)
        ''', (officer_id, status, timestamp, dna_hash, image_path))
        
        # Mirroring to Shadow Vault
        cursor.execute('''
            INSERT OR REPLACE INTO shadow_logs (officer_id, original_status, timestamp, dna_hash) 
            VALUES (?,?,?,?)
        ''', (officer_id, status, timestamp, dna_hash))
        
        conn.commit()
        print(f"--- [DB] SUCCESS: DNA for {officer_id} secured ---")
    except Exception as e:
        print(f"--- [DB] ERROR: {e} ---")
    finally:
        conn.close()

def save_document_record(officer_id, doc_name, doc_type, timestamp, file_dna, file_path):
    """Saves Binary DNA for Documents."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO document_vault (officer_id, doc_name, doc_type, timestamp, file_dna, file_path) 
            VALUES (?,?,?,?,?,?)
        ''', (officer_id, doc_name, doc_type, timestamp, file_dna, file_path))
        
        # Log Document state to Shadow Vault
        cursor.execute('''
            INSERT OR REPLACE INTO shadow_logs (officer_id, original_status, timestamp, dna_hash) 
            VALUES (?,?,?,?)
        ''', (officer_id, f"DOC:{doc_name}", timestamp, file_dna))
        
        conn.commit()
        print(f"--- [DB] SUCCESS: Document '{doc_name}' DNA locked ---")
    except Exception as e:
        print(f"--- [DB] ERROR: {e} ---")
    finally:
        conn.close()