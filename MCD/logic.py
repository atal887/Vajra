import hashlib
import numpy as np
import cv2
import os

def get_dna_hash(officer_id, status, timestamp):
    """
    Generates a unique 64-character forensic hex string (DNA).
    This string is treated as 512 bits (64 chars * 8 bits) for pixel hiding.
    """
    raw_data = f"{officer_id}|{status}|{timestamp}"
    # Using SHA-256 to generate a 64-character hex string
    sha_signature = hashlib.sha256(raw_data.encode()).hexdigest()
    return sha_signature

def stamp_image(img, dna_string):
    """
    Hides the 512-bit DNA string into the Least Significant Bits (LSB) 
    of the first 512 pixels of the image.
    """
    # Convert hex string to binary (8 bits per character = 512 bits total)
    binary_dna = "".join([format(ord(char), '08b') for char in dna_string])
    
    # Flatten image to access pixels sequentially
    flat_img = img.flatten()
    
    # Ensure image is large enough (at least 512 values)
    if len(flat_img) < 512:
        return img
        
    # Inject bits into the LSB of the first 512 pixel values
    for i in range(512):
        # Clear the last bit and set it to our DNA bit
        flat_img[i] = (flat_img[i] & ~1) | int(binary_dna[i])
        
    # Reshape back to original image dimensions
    return flat_img.reshape(img.shape)

def get_document_dna(file_path):
    """
    Generates a unique binary fingerprint for documents using Blake3/SHA-256.
    Detects any change in the physical file content.
    """
    if not os.path.exists(file_path):
        return "FILE_NOT_FOUND"
        
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read file in chunks to handle large documents
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
            
    return sha256_hash.hexdigest()

def verify_pixel_integrity(img_path, expected_dna):
    """
    Extraction logic to verify if the pixel-DNA has been tampered with.
    Matches the extraction logic used in analysis.py.
    """
    img = cv2.imread(img_path)
    if img is None:
        return False
        
    flat_img = img.flatten()
    # Extract first 512 bits
    extracted_bits = "".join([str(flat_img[i] & 1) for i in range(512)])
    
    # Convert bits back to hex string
    extracted_hash = ""
    for i in range(0, 512, 8):
        byte = extracted_bits[i:i+8]
        extracted_hash += chr(int(byte, 2))
        
    return extracted_hash.strip() == expected_dna