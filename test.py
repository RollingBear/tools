# -*- coding: utf-8 -*-

#   2019/5/31 0031 下午 6:04     

__author__ = 'RollingBear'

# import platform
# from ctypes import *
#
# if platform.system() == 'Windows':
#     libc = cdll.LoadLibrary('msvcrt.dll')
# elif platform.system() == 'Linux':
#     libc = cdll.LoadLibrary('libc.so.6')
#
# print('1->', libc.strchr('abcdefghij', c_char('d')))
#
# libc.strchr.restype = c_char_p
#
# print('2->', libc.strchr('abcdefghij', c_char('d')))
#
# print('3->', libc.strchr('abcdefghij', 'd'))
#
# libc.strchr.argtypes = [c_char_p, c_char]
# print('4->', libc.strchr('abcdefghij', 'd'))


from sympy import *
from math import radians, cos, sin, asin, sqrt

print(float(pi))