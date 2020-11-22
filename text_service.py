import socket
import argparse
import json
import sys
from socket import close
 
MAX_BYTES = 65536

class Server:

    def __init__(self, interface, port):
        self.interface = interface
        self.port = port
        self.start()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.interface,self.port))
        sock.listen(1)
        print('Listening at',sock.getsockname())
        n = 1
        while True:
            sc, sockname = sock.accept()
            data, file1, file2 = sc.recv(MAX_BYTES).decode('utf-8').split('$')
            if data == 'change_text':
                changingText = file1
                jsonText = file2
                jsonObj = json.loads(jsonText)
                for key in jsonObj:
                    changingText = changingText.replace(key, jsonObj[key])
                sc.send(changingText.encode())  
            elif data == 'encode_decode':
                answer = self.encrypt(file1, file2) if n%2 == 1 else self.decrypt(file1, file2)
                answer = answer.decode('utf-8')
                sc.send(str.encode("$".join([str(n), answer])))
                n+=1

    def encrypt(self, Text, keyword):
        i = 0
        cipherText = '' 
        while len(keyword)<len(Text):
            keyword += keyword
        for char in Text:
            if ord(char)>=65 and ord(char)<=90:
                if keyword[i].upper() != keyword[i]:
                    cipherText += chr((ord(keyword[i]) - 97 + (ord(char) - 65)) % 26 + 65)
                else:
                    cipherText += chr((ord(keyword[i]) - 65 + (ord(char) - 65)) % 26 + 65)
            elif ord(char)>=97 and ord(char)<=122:
                if keyword[i].upper() != keyword[i]:
                    cipherText += chr((ord(keyword[i]) - 97 + (ord(char) - 97)) % 26 + 97)
                else:
                    cipherText += chr((ord(keyword[i]) - 65 + (ord(char) - 97)) % 26 + 97)
            i+=1
        return cipherText.encode()

    def decrypt(self, Text, keyword):
        i = 0
        plainText = ''
        if len(keyword)<len(Text):
            while len(keyword)<len(Text):
                keyword += keyword
        for char in Text:
            if ord(char)>=65 and ord(char)<=90:
                if keyword[i].upper() != keyword[i]:
                    num = ord(char) - ord(keyword[i]) + 97
                    if num < 65:
                        num += 26
                    plainText += chr(num)
                else:
                    num = ord(char) - ord(keyword[i]) + 65
                    if num < 65:
                        num += 26
                    plainText += chr(num)
            elif ord(char)>=97 and ord(char)<=122:
                if keyword[i].upper() != keyword[i]:
                    num = ord(char) - ord(keyword[i]) + 97
                    if num < 97:
                        num += 26
                    plainText += chr(num)
                else:
                    num = ord(char) - ord(keyword[i]) + 65
                    if num < 97:
                        num += 26
                    plainText += chr(num)
            i+=1 
        return plainText.encode()

 
class Client:
    
    def __init__(self, hostname, port, mode, file1, file2):
        self.hostname = hostname
        self.port = port
        self.function = self.change_text if mode == 'change_text' else self.encode_decode
        self.function(file1,file2)

    def change_text(self, file1, file2):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.hostname,self.port))
        originalFile = open(file1,'r')
        file1Text = originalFile.read()
        originalFileName = originalFile.name.split('.txt')[0]
        originalFile.close()
        jsonFile = open(file2, 'r')
        file2Text = jsonFile.read()
        jsonFile.close()
        sock.send(str.encode("$".join(['change_text', file1Text, file2Text])))
        changedText = sock.recv(MAX_BYTES)
        newFile = open(originalFileName + '_Modified.txt', 'wb')
        newFile.write(changedText)
        newFile.close()

    def encode_decode(self, file1, file2):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.hostname,self.port))
        originalFile = open(file1,'r')
        file1Text = originalFile.read()
        originalFileName = originalFile.name.split('.txt')[0]
        originalFile.close()
        keywordFile = open(file2, 'r')
        file2Text = keywordFile.read()
        keywordFile.close()
        sock.send(str.encode("$".join(['encode_decode', file1Text, file2Text])))
        mode, changedText = sock.recv(MAX_BYTES).decode('utf-8').split('$')
        mode = int(mode)
        newFile = open(originalFileName + '_Encrypted.txt', 'w') if mode%2 == 1 else open(originalFileName + '_Decrypted.txt', 'w')
        newFile.write(changedText)
        newFile.close()
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send file to the server')
    parser.add_argument('--server', action= 'store_true')
    parser.add_argument('-p',type = int, default = 1060,
                        help ='TCP port number ( default = %(default)s)')
    parser.add_argument('--hostname', default ='127.0.0.1',
                        help='IP address or hostname ( default = %(default)s)')
    parser.add_argument('--mode', type = str, dest = 'Mode', choices= ('change_text', 'encode_decode'),
                        help='Mode of client request followed by paths to both files')
    if '--mode' in sys.argv:
        parser.add_argument('file1', help='Path to file 1')
        parser.add_argument('file2', help='Path to file 2')
    args = parser.parse_args()
    if args.Mode:
        try:
            clientObj = Client(args.hostname, args.p, args.Mode, args.file1, args.file2)
        except ConnectionRefusedError:
            parser.error("Wrong order of arguments")
    else:
        serverObj = Server(args.hostname, args.p)