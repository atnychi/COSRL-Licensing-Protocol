import json
import hashlib
import sys
import datetime

# === Configurable Paths ===
MANIFEST_FILE = "activation_manifest.yaml"
TOLL_REGISTRY = "toll_registry.json"
SYSTEM_ID_FIELD = "system_id"

# === Load System ID from Manifest ===
def load_system_id(manifest_path):
    import yaml
    with open(manifest_path, "r") as f:
        manifest = yaml.safe_load(f)
    return manifest.get(SYSTEM_ID_FIELD)

# === Load Toll Registry ===
def load_toll_registry():
    try:
        with open(TOLL_REGISTRY, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[COSRL] Toll registry not found.")
        return {}

# === Check Toll Validity ===
def validate_toll(system_id, registry):
    if system_id not in registry:
        return False
    record = registry[system_id]
    expiry = record.get("expiry")
    if expiry:
        expiry_date = datetime.datetime.strptime(expiry, "%Y-%m-%d")
        return expiry_date >= datetime.datetime.now()
    return True

# === Main Validator Logic ===
def main():
    system_id = load_system_id(MANIFEST_FILE)
    if not system_id:
        print("[COSRL] ERROR: System ID not found in manifest.")
        sys.exit(1)

    registry = load_toll_registry()
    if not validate_toll(system_id, registry):
        print(f"[COSRL] SYSTEM IN BREACH: {system_id} is not toll-compliant.")
        sys.exit(1)

    print(f"[COSRL] VALID: {system_id} is toll-cleared.")

if __name__ == "__main__":
    main()
