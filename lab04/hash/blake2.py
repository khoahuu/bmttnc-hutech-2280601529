import hashlib

def blake2(message):
    blake2_hash = hashlib.blake2b(digest_size=64)
    blake2_hash.update(message)
    return blake2_hash.digest()
def main():
    text = input("Nhập chuỗi cần băm: ").encode('utf-8')
    hashed_text = blake2(text)
    print("chuỗi văn bản đã nhập:", text.decode('utf-8'))
    print("BLAKE2 hash:", hashed_text.hex())
if __name__ == "__main__":
    main()