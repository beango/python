import sys
import telnetlib

tn = telnetlib.Telnet("104.128.81.9")


tn.read_until(b"Username :", 2)
tn.write(b"\n")

tn.read_until(b"Password :", 2)
tn.write(b"\n")

tn.read_until(b"=>", 2)
tn.write(b"exit\n")

tn.close