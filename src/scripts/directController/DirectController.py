import sys
import os
from jinja2 import Template
import subprocess
import json

from ..config import *
from ..entity import *
from ..util import *


class DirectController:

    @staticmethod
    def uploadCpp():
        pass

    @staticmethod
    def uploadHpp():
        pass

    @staticmethod
    def updateServiceJson():
        pass

    @staticmethod
    def generateAtomService() -> json:
        pass

    @staticmethod
    def generateGrpcServer() -> json:
        pass

    @staticmethod
    def startProgram():
        pass

    @staticmethod
    def shutProgram():
        pass
