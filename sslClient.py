import socket
import ssl
import sys
from dataFile import *
from Crypto.Cipher import AES 
from Crypto.Hash import SHA256 
from Crypto import Random 

context = ssl.create_default_context()

conn = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname='')
conn.connect(('', 9500))
cert = conn.getpeercert()

def encrypt(key, filename):
    chunksize = 64*1024
    outputFile = "(encrypted)"+filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0: 
                    chunk +=b'' * (16- (len(chunk) %16))
                    outfile.write(encryptor.encrypt(chunk))
    return outputFile

def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()


conn.sendall(outputFile)