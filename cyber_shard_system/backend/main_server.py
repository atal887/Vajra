from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import hashlib
from datetime import datetime
import threading
import time

from encryption import generate_key, encrypt_data, decrypt_data
from sharding import split_into_shards, generate_parity

app = Flask(__name__)
CORS(app)

SERVERS = [
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",
    "http://127.0.0.1:5003"
]

documents = {}
stored_keys = {}

# ===============================
# Utility Functions
# ===============================

def fetch_shard(server_url, filename):
    try:
        response = requests.get(f"{server_url}/get/{filename}")
        if response.status_code == 200:
            return response.content
    except:
        pass
    return None


def reconstruct_shards(doc_id):
    filenames = [
        f"{doc_id}_shard0.bin",
        f"{doc_id}_shard1.bin",
        f"{doc_id}_shard2.bin"
    ]

    shard1 = fetch_shard(SERVERS[0], filenames[0])
    shard2 = fetch_shard(SERVERS[1], filenames[1])
    parity = fetch_shard(SERVERS[2], filenames[2])

    # Try reconstruct shard1
    if shard1 is None and shard2 and parity:
        if len(shard2) != len(parity):
            return None, None
        shard1 = bytes(a ^ b for a, b in zip(shard2, parity))

    # Try reconstruct shard2
    if shard2 is None and shard1 and parity:
        if len(shard1) != len(parity):
            return None, None
        shard2 = bytes(a ^ b for a, b in zip(shard1, parity))

    return shard1, shard2


def internal_verify(doc_id):
    shard1, shard2 = reconstruct_shards(doc_id)

    if shard1 is None or shard2 is None:
        documents[doc_id]["status"] = "compromised"
        return False

    encrypted = shard1 + shard2
    calculated_hash = hashlib.sha256(encrypted).hexdigest()

    if calculated_hash != documents[doc_id]["hash"]:
        documents[doc_id]["status"] = "compromised"
        return False

    documents[doc_id]["status"] = "active"
    return True


# ===============================
# Routes
# ===============================

@app.route("/ping")
def ping():
    return "PING WORKING"

@app.route("/seed", methods=["POST"])
def seed_documents():
    data = request.json
    for doc in data:
        documents[doc["id"]] = {
            "id": doc["id"],
            "name": doc["name"],
            "department": doc["department"],
            "status": "active",
            "lastModified": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    return jsonify({"message": "Seeded"})


@app.route("/documents", methods=["GET"])
def get_documents():
    return jsonify(list(documents.values()))


@app.route("/upload/<doc_id>", methods=["POST"])
def upload_document(doc_id):
    if doc_id not in documents:
        return jsonify({"error": "Document not found"}), 404

    data = request.json["content"].encode()

    key = generate_key()
    stored_keys[doc_id] = key

    encrypted = encrypt_data(data, key)
    hash_value = hashlib.sha256(encrypted).hexdigest()
    documents[doc_id]["hash"] = hash_value

    shard1, shard2 = split_into_shards(encrypted, 2)
    parity = generate_parity(shard1, shard2)

    for i, shard in enumerate([shard1, shard2, parity]):
        files = {"file": (f"{doc_id}_shard{i}.bin", shard)}
        requests.post(f"{SERVERS[i]}/store", files=files)

    documents[doc_id]["status"] = "active"
    documents[doc_id]["lastModified"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return jsonify({"message": "Stored Distributed"})


@app.route("/view/<doc_id>", methods=["GET"])
def view_document(doc_id):
    if doc_id not in documents:
        return jsonify({"error": "Document not found"}), 404

    if not internal_verify(doc_id):
        return jsonify({"error": "Integrity check failed"}), 500

    shard1, shard2 = reconstruct_shards(doc_id)
    encrypted = shard1 + shard2
    decrypted = decrypt_data(encrypted, stored_keys[doc_id])

    return jsonify({
        "content": decrypted.decode(),
        "status": documents[doc_id]["status"]
    })


@app.route("/recover/<doc_id>", methods=["POST"])
def recover_document(doc_id):
    if doc_id not in documents:
        return jsonify({"error": "Document not found"}), 404

    filenames = [
        f"{doc_id}_shard0.bin",
        f"{doc_id}_shard1.bin",
        f"{doc_id}_shard2.bin"
    ]

    shard1 = fetch_shard(SERVERS[0], filenames[0])
    shard2 = fetch_shard(SERVERS[1], filenames[1])
    parity = fetch_shard(SERVERS[2], filenames[2])

    # Reconstruct and write back
    if shard1 is None and shard2 and parity:
        shard1 = bytes(a ^ b for a, b in zip(shard2, parity))
        files = {"file": (filenames[0], shard1)}
        requests.post(f"{SERVERS[0]}/store", files=files)

    if shard2 is None and shard1 and parity:
        shard2 = bytes(a ^ b for a, b in zip(shard1, parity))
        files = {"file": (filenames[1], shard2)}
        requests.post(f"{SERVERS[1]}/store", files=files)

    documents[doc_id]["status"] = "active"
    return jsonify({"message": "Shard Reconstructed and Recovered"})


@app.route("/verify/<doc_id>", methods=["GET"])
def verify_route(doc_id):
    if doc_id not in documents:
        return jsonify({"error": "Document not found"}), 404

    result = internal_verify(doc_id)

    if result:
        return jsonify({"status": "verified"})
    else:
        return jsonify({"status": "compromised"})


@app.route("/simulate-delete/<doc_id>", methods=["DELETE"])
def simulate_delete(doc_id):
    # Delete shard1 from server2 only (simulate single failure)
    try:
        os.remove(f"storage_server2/storage/{doc_id}_shard1.bin")
    except:
        pass

    documents[doc_id]["status"] = "compromised"
    return jsonify({"message": "Shard deleted to simulate failure"})


# ===============================
# Background Auditor
# ===============================

def background_verifier():
    while True:
        for doc_id in list(documents.keys()):
            internal_verify(doc_id)
        time.sleep(10)

threading.Thread(target=background_verifier, daemon=True).start()


if __name__ == "__main__":
    app.run(port=8010)