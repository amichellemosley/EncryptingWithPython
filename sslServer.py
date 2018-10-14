import socket
import ssl
import sys
from Crypto.Cipher import AES 
from Crypto.Hash import SHA256 
from Crypto import Random 


context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="mycertfile", keyfile="mykeyfile")

bindsocket = socket.socket()
bindsocket.bind(('', 9500))
bindsocket.listen(5)

while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = context.wrap_socket(newsocket, server_side=True)
    try:
       decrypt(connstream)
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()

def decrypt(key,filename,connstream):
    chunksize = 64*1024
    outputFile = filename[11:]
    data = connstream.recv(4069)

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)
        with open(outputFile, 'wb') as outfile:
            while True: 
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)
    return outfile

def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()