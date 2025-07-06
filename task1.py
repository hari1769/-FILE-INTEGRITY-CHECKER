import hashlib
import os
import json
import time


MONITOR_PATH = "./files_to_monitor"
HASH_STORE = "file_hashes.json"


def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None


def load_hashes():
    if os.path.exists(HASH_STORE):
        with open(HASH_STORE, 'r') as f:
            return json.load(f)
    return {}


def save_hashes(hashes):
    with open(HASH_STORE, 'w') as f:
        json.dump(hashes, f, indent=4)


def monitor_files():
    previous_hashes = load_hashes()
    current_hashes = {}

    print("\n🔎 Scanning files for changes...\n")

    for root, _, files in os.walk(MONITOR_PATH):
        for file in files:
            path = os.path.join(root, file)
            file_hash = calculate_hash(path)
            current_hashes[path] = file_hash

          
            if path not in previous_hashes:
                print(f"[NEW] File added: {path}")
            elif previous_hashes[path] != file_hash:
                print(f"[MODIFIED] File changed: {path}")

    
    for path in previous_hashes:
        if path not in current_hashes:
            print(f"[DELETED] File removed: {path}")

    
    save_hashes(current_hashes)
    print("\n✅ Monitoring complete.\n")


if __name__ == "__main__":
    print("🛡️ File Integrity Checker - Using SHA256\n")
    os.makedirs(MONITOR_PATH, exist_ok=True)
    monitor_files()