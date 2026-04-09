import sqlite3

# Database Path
DB_PATH = 'mcd_records.db'

def hack_fourth_record():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Skip the first 3 records and grab the 4th one (ORDER BY timestamp ASC)
    # LIMIT 1 OFFSET 3 means "Give me 1 row, but skip the first 3"
    cursor.execute("SELECT officer_id FROM reports ORDER BY timestamp ASC LIMIT 1")
    row = cursor.fetchone()
    
    if not row:
        print("\n--- ❌ ERROR: Not enough records! ---")
        print("Bhai, make sure you have at least 4 records in the Dashboard first.")
        conn.close()
        return

    target_id = row[0]
    fake_status = "BRIBED / RECORD DELETED"
    
    print(f"\n--- 😈 TARGETING THE 4TH FORENSIC RECORD: {target_id} ---")
    
    try:
        # 2. Database Metadata hijacking
        cursor.execute("UPDATE reports SET status = ? WHERE officer_id = ?", (fake_status, target_id))
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"--- ✅ HACK SUCCESSFUL: {target_id} (The 4th Row) is now corrupted. ---")
            print("--- (Forensic DNA mismatch will trigger on next audit) ---")
        else:
            print(f"--- ❌ ERROR: Could not find or update the 4th record. ---")
            
    except sqlite3.Error as e:
        print(f"--- ❌ SQL Error: {e} ---")
        
    conn.close()

if __name__ == "__main__":
    hack_fourth_record()