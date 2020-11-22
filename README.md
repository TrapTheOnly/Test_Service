# Test Service App

## Table Of Contents
1. [About](https://github.com/TrapTheOnly/Test_Service#about-app)
2. [Installation](https://github.com/TrapTheOnly/Test_Service#installation)
3. [Usage Guide](https://github.com/TrapTheOnly/Test_Service#usage-guide)

## About App

* Change text: The sender sends the text file and the json file to the server. In respond, the server
must read the json file and swap the words from the text according to it.

* Encode/Decode text: The sender sends the text file and the key (another text). In respond,
the server must XOR the text message with the key (One Time Pad cipher) and return it to the
client. The decrypting process happens in the same way, but instead of the text message, the
client sends the cipher text. Client on odd-numbered request encodes and on even-numbered request decodes.

## Installation

In terminal window enter:
```
git clone https://github.com/TrapTheOnly/Test_Service.git
```

To install requirements in terminal window enter:
```C++
pip install -r requirements.txt
```

## Usage Guide

You need at least 2 seperate terminals being open:

Server Terminal
```C++
python3 test_service.py --hostname {Hostname} -p {Port number}
```

Client Terminal
```C++
python3 test_service.py [-h] [-p P] [--hostname HOSTNAME] [--mode {change_text,encode_decode}] file1 file2
```

By default Hostname is set to `127.0.0.1`

By default Port number is set to `65432`

In client terminal ```--mode``` argument is necessary

After entering ```--mode``` argument, ```file1``` and ``` file2``` arguments are also necessary

```file1``` and ```file2``` arguments have to contain the address of required files:

* In ```--mode change_text```:
  * file1 = some ```.txt``` format file that has to be changed
  * file2 = some ```.json``` format file that has to be used to repalce text
* In ```--mode enrypt_decrypt```:
  * When encrypting: 
    * file1 = some ```.txt``` format file that has to be encrypted
    * file2 = some ```.txt``` format file that has to contain key for encrypting
  * When decrypting:
    * file1 = some ```.txt``` format file that has to be decrypted
    * file2 = some ```.txt``` format file that has to contain key for decrypting    

To stop server, head to Server Terminal and press ``Ctrl+C`` in terminal.