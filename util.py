import os
import sys
import subprocess
import json
import logging as fflogger
fflogger.basicConfig(format = "[%(levelname)s: %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s]", level=fflogger.DEBUG)

class Command():

    _stdout = None
    _stderr = None 
    _returncode: int = None

    @property
    def stdout(self):
        return self._stdout
    
    @property
    def stderr(self):
        return self._stderr
    
    @property
    def returncode(self):
        return self._returncode

    def __init__(self, command: list):
        self._command = command

    def execute(self):
        process = subprocess.Popen(self._command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        out, err = process.communicate()
        self._returncode = process.returncode
        self._stdout = out
        if self._returncode != 0:
            self._stderr = err