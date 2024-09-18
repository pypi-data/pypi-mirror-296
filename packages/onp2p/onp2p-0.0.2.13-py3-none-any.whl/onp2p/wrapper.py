from cffi import FFI
import os

ffi = FFI()

# Dichiarazioni delle funzioni C che vogliamo esporre a Python
ffi.cdef("""
    int add(int a, int b);
    int multiply(int a, int b);
    int create_channel(int port);
""")


# Carichiamo la libreria C compilata
current_dir = os.path.dirname(__file__)
lib_path = os.path.join(current_dir, "libmath_operations.so")
lib_path_tor = os.path.join(current_dir, "libtor_operations.so")

# Carica la libreria
C = ffi.dlopen(lib_path)
TOR = ffi.dlopen(lib_path_tor)


# Wrapper per esporre le funzioni a Python
def add(a, b):
    return C.add(a, b)

def multiply(a, b):
    return C.multiply(a, b)


def create_channel(port):
    return TOR.create_channel(port)


