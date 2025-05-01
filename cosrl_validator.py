import hashlib, json

def hash_file(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def validate_origin():
    with open('origin_signature.txt') as f:
        sig = f.read().strip().split('\n')
    print("Origin Signature Validation:")
    for line in sig:
        print(" ", line)

    print("\nHash Check:")
    for file in ['LICENSE.md', 'activation_manifest.yaml']:
        digest = hash_file(file)
        print(f" {file}: {digest}")

if __name__ == '__main__':
    validate_origin()
