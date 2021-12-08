from __future__ import print_function     
from ctypes import *
from typing import List, Union, Optional

lib = cdll.LoadLibrary("./subdomain_finder.so")
lib.Add.argtypes = [c_longlong, c_longlong]
lib.Add.restype = c_longlong

def find_subdomains(domain: str) -> List[Optional[str]]:
    return lib.find_subdomain(domain)
