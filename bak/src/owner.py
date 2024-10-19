from .developer import Developer
from .maintainer import Maintainer

class Owner:
    def __init__(self, developer: Developer, maintainer: Maintainer):
        self.developer = developer
        self.maintainer = maintainer