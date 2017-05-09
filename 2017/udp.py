import socket  
  
address = ('192.168.242.101', 8001)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
  
 
msg = "00410"
s.sendto(msg, address)  
  
s.close()  