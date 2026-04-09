import sqlite3
import os

# Database Path
DB_PATH = 'mcd_records.db'

def hack_document():
    print("\n" + "="*50)
    print("⚠️  MCD MALWARE SIMULATOR: INITIATING BINARY ATTACK")
    print("="*50)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # UPDATED: Fetching using officer_id instead of id
        cursor.execute("SELECT officer_id, doc_name, file_path FROM document_vault LIMIT 1")
        result = cursor.fetchone()

        if result:
            off_id, doc_name, file_path = result
            
            if os.path.exists(file_path):
                print(f"[ATTACK] Target Found: {doc_name} (Officer: {off_id})")
                
                # Malicious Action: Overwriting the file with garbage data
                with open(file_path, "a") as f:
                    f.write("\n--- HACKED BY UNAUTHORIZED ENTITY ---")
                
                print(f"[SUCCESS] Binary DNA corrupted for: {file_path}")
                print(f"[STATUS] Audit system should now trigger a CRITICAL ALERT.")
            else:
                print(f"[ERROR] Physical file not found at: {file_path}")
        else:
            print("[ERROR] No documents found in the vault to hack.")

    except sqlite3.OperationalError as e:
        print(f"[DB ERROR] {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    confirm = input("Confirm Binary Attack Simulation? (y/n): ")
    if confirm.lower() == 'y':
        hack_document()
    else:
        print("Attack aborted.")