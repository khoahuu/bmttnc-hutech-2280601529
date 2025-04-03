import base64
def main():
    input_string = input("nhập thông tin cần mã hoá: ")
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    
    with open("data.txt", "w") as file:
        file.write(encoded_string)
    print("Mã hoá thành công và đã lưu vào data.txt")
if __name__ == "__main__":
    main()
    