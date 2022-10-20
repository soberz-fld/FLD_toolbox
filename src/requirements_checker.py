import pip
import inspect
import os

from fldlogging import log

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))
#TODO: Check path if used from another project

if os.name == 'nt':  # Windows
    requirements_txt_path = path + '\\' + 'requirements.txt'
elif os.name == 'posix':  # Linux
    requirements_txt_path = path + '/' + 'requirements.txt'
else:
    requirements_txt_path = 'requirements.txt'

with open(requirements_txt_path, mode='r') as req_file:
    dependencies = req_file.read().splitlines()
    for dependency in dependencies:
        try:
            __import__(dependency)
        except ImportError:
            pip.main(['install', dependency])
