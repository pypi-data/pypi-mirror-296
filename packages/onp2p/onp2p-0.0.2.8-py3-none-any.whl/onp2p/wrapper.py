from cffi import FFI

ffi = FFI()

# Dichiarazioni delle funzioni C che vogliamo esporre a Python
ffi.cdef("""
    int add(int a, int b);
    int multiply(int a, int b);
""")


# Carichiamo la libreria C compilata
current_dir = os.path.dirname(__file__)
lib_path = os.path.join(current_dir, "libmath_operations.so")

# Carica la libreria
C = ffi.dlopen(lib_path)


# Wrapper per esporre le funzioni a Python
def add(a, b):
    return C.add(a, b)

def multiply(a, b):
    return C.multiply(a, b)


