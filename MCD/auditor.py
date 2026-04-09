import sqlite3
import cv2
from logic import get_dna_hash

def extract_hash_from_pixels(image_path):
    """Extracts the 512-bit hash hidden in the image pixels."""
    img = cv2.imread(image_path)
    if img is None: return None
    flat_img = img.flatten()
    binary_data = "".join([str(flat_img[i] & 1) for i in range(512)])
    return "".join([chr(int(binary_data[i:i+8], 2)) for i in range(0, 512, 8)])

def manual_audit():
    print("\n--- 🧐 MCD MANUAL AUDIT TOOL ---")
    off_id = input("Enter Officer ID to verify: ")

    conn = sqlite3.connect('mcd_records.db')
    cursor = conn.cursor()
    
    # Check the main table
    cursor.execute("SELECT status, timestamp, dna_hash, image_path FROM reports WHERE officer_id = ?", (off_id,))
    row = cursor.fetchone()

    if row:
        status, ts, db_hash, img_path = row
        print(f"\n[📁] Database Entry Found: Status='{status}' | Time='{ts}'")
        
        # Extract truth from pixels
        pixel_hash = extract_hash_from_pixels(img_path)
        # Recalculate hash based on current DB text
        current_calc_hash = get_dna_hash(off_id, status, ts)

        if pixel_hash == current_calc_hash:
            print("✅ VERIFICATION SUCCESS: Database matches Image DNA.")
        else:
            print("🚨 VERIFICATION FAILED: Database does not match Image DNA!")
            
            # Fetch truth from Shadow Logs for the user
            cursor.execute("SELECT original_status FROM shadow_logs WHERE officer_id = ?", (off_id,))
            original = cursor.fetchone()
            if original:
                print(f"🔍 SHADOW VAULT ANALYSIS: The original status was '{original[0]}'")
                
                fix = input("\nWould you like to manually restore this record? (y/n): ").lower()
                if fix == 'y':
                    cursor.execute("UPDATE reports SET status = ? WHERE officer_id = ?", (original[0], off_id))
                    conn.commit()
                    print("🛠️ Record restored successfully.")
    else:
        print("❌ No record found for that Officer ID.")

    conn.close()

if __name__ == "__main__":
    manual_audit()