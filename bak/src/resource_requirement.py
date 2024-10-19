class ResourceRequirement:
    def __init__(self, cpu_architecture: str, memory: int, hard_disk: int):
        self.cpu_architecture = cpu_architecture
        self.memory = memory
        self.hard_disk = hard_disk