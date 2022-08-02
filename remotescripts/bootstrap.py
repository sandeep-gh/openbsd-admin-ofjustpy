# install necessary stuff (like, wget, pip, python-packages so that rest of code can run

import os
import sys
from subprocess import Popen, PIPE
from utils import exec_cmd
from config import project_root
import os
import pickle
exec_cmd(["doas",  "pkg_add", "py3-pip", "git"])
exec_cmd(["pip3", "install", "clustershell", "wget", "psutil", "gitpython"])

exec_cmd(["doas", "mkdir",  "/home/shared"])
exec_cmd([
            "doas", "mkdir",  "/home/shared/itadmin"
    ])

exec_cmd([
             "mkdir",  "/home/shared/itadmin"
    ])

exec_cmd(["doas", "groupadd", "-g",  "1003",  "shared"])
exec_cmd(["doas", "usermod", "-G", "shared", "adming"])
exec_cmd(["doas",  "chown",  "-R", "adming:shared",  "/home/shared"])

exec_cmd([
             "mkdir",  "/home/shared/itadmin"
    ])


# initialize the env bookkeeping
env_fp = f"{project_root}/itadmin/env.pickle"
if not os.path.exists(env_fp):
    env = {}
    with open(env_fp, "wb") as fh:
        pickle.dump(env, fh)

        

