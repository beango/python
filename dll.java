from ctypes import *


dll = windll.LoadLibrary('E:\code\lx_code\dlltest.dll')

print(dll)

a=dll.Double(123)
print(type(a))
print(a)
