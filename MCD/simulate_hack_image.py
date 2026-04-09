import sqlite3
import cv2
import numpy as np
import os

# Database Path
DB_PATH = 'mcd_records.db'

def hack_image_file():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # FIX: 'id' hata diya gaya hai, 'timestamp' ke basis par latest record uthao
    try:
        cursor.execute("SELECT officer_id, image_path FROM reports ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()
    except sqlite3.OperationalError:
        print("[!] Database schema mismatch. Make sure reports table exists.")
        conn.close()
        return
    
    if not row:
        print("[!] No image records found to hack.")
        conn.close()
        return

    off_id, img_path = row
    
    print(f"\n--- 😈 INITIALIZING IMAGE PIXEL HACK ---")
    print(f"Targeting Asset for Officer: {off_id}")
    print(f"File Path: {img_path}")

    if os.path.exists(img_path):
        # Asli image ko read karo
        img = cv2.imread(img_path)
        
        # PIXEL TAMPERING: Top-left corner mein black box
        # Isse LSB-embedded DNA bits poori tarah destroy ho jayenge
        cv2.rectangle(img, (0, 0), (150, 150), (0, 0, 0), -1) 
        
        # Tampered image ko overwrite karo
        cv2.imwrite(img_path, img)
        
        print(f"✅ [SUCCESS] Pixels corrupted for {off_id}. DNA signature is now invalid.")
    else:
        print(f"❌ Error: Physical image file not found at {img_path}")

    conn.close()
    print("\n--- 🏁 IMAGE HACK COMPLETE. Check Dashboard for RED ALERT. ---")

if __name__ == "__main__":
    hack_image_file()