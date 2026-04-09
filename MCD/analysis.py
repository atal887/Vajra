import sqlite3
import cv2
import os
import time
from logic import get_dna_hash, get_document_dna

# Absolute path for stability on your MacBook Air
db_path = os.path.join(os.path.dirname(__file__), 'mcd_records.db')

def extract_hash_from_image(image_path):
    """
    Extracts the hidden 512-bit forensic DNA from image pixels.
    Matches the LSB injection logic in logic.py.
    """
    if not os.path.exists(image_path):
        return None
        
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    # Flatten image and extract LSB from the first 512 values
    flat_img = img.flatten()
    bit_count = 512 
    binary_data = "".join([str(flat_img[i] & 1) for i in range(bit_count)])
    
    # Convert 512 bits back into the 64-character hex string
    extracted_hash = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        extracted_hash += chr(int(byte, 2))
    
    return extracted_hash.strip()

def run_audit():
    """
    Scans the registry and physical vault for unauthorized changes.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\n" + "="*60)
    print("MCD FORENSIC AUDIT: MONITORING ASSET INTEGRITY")
    print("="*60)

    # --- 1. IMAGE AUDIT: Checks Pixel DNA and Metadata ---
    # Querying using officer_id as the primary key
    cursor.execute("SELECT officer_id, status, timestamp, dna_hash, image_path FROM reports")
    
    for rec in cursor.fetchall():
        off_id, db_status, db_time, db_hash, img_path = rec
        
        # Verify physical pixel integrity
        pixel_truth = extract_hash_from_image(img_path)
        # Calculate what the DNA should be based on current DB record
        expected = get_dna_hash(off_id, db_status, db_time)
        
        # If pixels or DB hash don't match the logic, we have a breach
        if pixel_truth != expected or db_hash != expected:
            print(f"[ALERT] FORENSIC MISMATCH | Officer: {off_id}")
            
            # Cross-verify with the Immutable Shadow Vault
            cursor.execute("SELECT original_status FROM shadow_logs WHERE officer_id=?", (off_id,))
            result = cursor.fetchone()
            
            if result:
                orig_status = result[0]
                # If the DB status was changed by a hacker, auto-repair it
                if orig_status != db_status:
                    print(f"ANALYSIS: Unauthorized Registry Modification detected.")
                    print(f"ACTION: Restoring original status: '{orig_status}'")
                    cursor.execute("UPDATE reports SET status = ? WHERE officer_id = ?", (orig_status, off_id))
                    conn.commit()
                    print("STATUS: Registry repaired via Shadow Vault.")
                else:
                    print("ANALYSIS: Registry is intact but the physical IMAGE file is corrupted.")
        else:
            print(f"VERIFIED: Image DNA secure for {off_id}")

    # --- 2. DOCUMENT AUDIT: Checks Binary Fingerprints ---
    try:
        cursor.execute("SELECT officer_id, doc_name, file_dna, file_path FROM document_vault")
        for doc in cursor.fetchall():
            off_id, d_name, stored_dna, d_path = doc
            fresh_dna = get_document_dna(d_path)
            
            if fresh_dna != stored_dna:
                print(f"[CRITICAL] DOCUMENT TAMPERED: {d_name}")
                print(f"STATUS: Binary DNA mismatch detected in file system.")
            else:
                print(f"VERIFIED: Document binary secure for {d_name}")
                
    except Exception as e:
        print(f"AUDIT INFO: {e}")

    conn.close()

if __name__ == "__main__":
    try:
        # Runs a full system scan every 10 seconds
        while True:
            run_audit()
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nAudit Monitor Terminated.")