import ctypes

import os

class LogicCoreBridge:

"""

Python ctypes wrapper for the Native C Core.

Allows for high-performance integration in scripting environments.

"""

def __init__(self, seed, complexity=1, lib_path="./build/lib4ndr0_core.so"):

if not os.path.exists(lib_path):

raise FileNotFoundError(f"Native Library not found at {lib_path}")

self.lib = ctypes.CDLL(os.path.abspath(lib_path))

self.lib.logic_core_init.restype = ctypes.c_void_p

self.lib.logic_core_transform.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]

self.lib.logic_core_destroy.argtypes = [ctypes.c_void_p]

self.ctx = self.lib.logic_core_init(seed, complexity)

def transform(self, data: str) -> str:

b_data = data.encode('utf-8')

buffer = ctypes.create_string_buffer(b_data, len(b_data))

self.lib.logic_core_transform(self.ctx, buffer, len(b_data))

return buffer.raw.hex()

def __del__(self):

if hasattr(self, 'lib') and hasattr(self, 'ctx'):

self.lib.logic_core_destroy(self.ctx)
