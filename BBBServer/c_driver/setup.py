
from distutils.core import setup, Extension
setup(name="c_driver",version="1.0",py_modules = ["c_driver.py"],ext_modules = [Extension("c_driver",["py_c_driver.c","c_driver.c"])])
