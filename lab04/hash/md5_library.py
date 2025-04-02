import hashlib

def calculate_md5(input_string):
    """
    Calculate the MD5 hash of the input string.

    Args:
        input_string (str): The string to be hashed.

    Returns:
        str: The MD5 hash of the input string in hexadecimal format.
    """
    # Create an MD5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the bytes of the input string
    md5_hash.update(input_string.encode('utf-8'))

    # Return the hexadecimal digest of the hash
    return md5_hash.hexdigest()
input_string = input("Enhập chuỗi cần băm: ")
md5_hash = calculate_md5(input_string)  
print("Mã băm MD5 của chuỗi '{}' là: {}".format(input_string, md5_hash))