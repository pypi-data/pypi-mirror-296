def decrypt():
    import os
    from cryptography.fernet import Fernet
    current_file_path = os.path.abspath(__file__)

    files = []

    for file in os.listdir():
        file_path = os.path.abspath(file)
        
        if file_path == current_file_path or file == "thekey.key" or file == "de.py":
            continue
        if os.path.isfile(file):
            files.append(file)
    
    print(files)
    
    with open("thekey.key", "rb") as key_file:
        decrypt_key = key_file.read()
    
    key = "key"
    user_key = input("Enter the key: ")
    
    if key == user_key:
        for file in files:
            file_path = os.path.abspath(file)
            with open(file_path, "rb") as thefile:
                content = thefile.read()
                decrypted_content = Fernet(decrypt_key).decrypt(content)
    
            with open(file_path, "wb") as thefile:
                thefile.write(decrypted_content)
                print(f"Decrypted file: {file_path}")
                print("Key:", decrypt_key)
    else:
        print("Wrong key! Try again...")