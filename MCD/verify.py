import cv2
import numpy as np

def extract_hash(image_path):
    # Read the secured image
    img = cv2.imread(image_path)
    if img is None:
        return "File not found!"
        
    flat_img = img.flatten()
    
    # Extract the first 512 bits (64 chars * 8 bits)
    binary_data = ""
    for i in range(512):
        binary_data += str(flat_img[i] & 1)
    
    # Convert bits to string
    chars = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]
    return "".join(chars)

if __name__ == "__main__":
    file_to_check = input("Enter the full name of the secured file (e.g., secured_IND_123.png): ")
    hidden_dna = extract_hash(file_to_check)
    print(f"\n[RESULT] Hidden DNA extracted from pixels:\n{hidden_dna}")