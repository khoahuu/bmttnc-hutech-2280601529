import hashlib
def calculate_sha256_hash(data):
    sha256_hash= hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    return sha256_hash.hexdigest()
data_to_hash = input("nhập dữ liệu cần băm: ")
hash_value = calculate_sha256_hash(data_to_hash)
print("Giá trị băm SHA-256 của dữ liệu '{}' là: {}".format(data_to_hash, hash_value))