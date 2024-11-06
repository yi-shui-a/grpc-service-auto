import sys
import os


sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import Server


class ServerUtil:
    def __init__(self):
        self.server: Server.Server = None

    def generateServerJson(self):
        pass

    def generateAsyncServer(self):
        pass

    def generateSyncServer(self):
        pass

    def generateClient(self):
        pass
