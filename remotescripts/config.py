from enum import Enum, auto

CXX = "/usr/bin/c++"
base_dir = "/home/shared"
project_root = base_dir
default_pg_port = 6976

class MachineType(Enum):
    development=auto()
    production=auto()
    configuration=auto()
    db = auto()
    mediawiki= auto()
    
targetmachine_type = MachineType.production
