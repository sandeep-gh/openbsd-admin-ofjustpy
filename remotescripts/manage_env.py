import sys
from config import project_root
#sys.path.append(f"{project_root}/itadmin/")
import pickle
import os

env_fp = f"{project_root}/itadmin/env.pickle"

# def add_to_env(varname, path):
#     with open(env_fp, "rb") as fh:
#         envvars = pickle.load(fh)

#     if varname in envvars.keys():
#         if path not in envvars[varname]:
#             envvars[varname].append(path)
#     else:
#         envvars[varname] = []
#         envvars[varname].append(path)
#     print(envvars)
#     with open(env_fp, "wb") as fh:
#         pickle.dump(envvars, fh)


def build_env():
    with open(env_fp, "rb") as fh:
        envvars = pickle.load(fh)
    env_str = "\n".join(
        [f"""{key}={":".join(envvars[key])}:${key}""" for key in envvars.keys()])
    return env_str

# if not os.path.exists(env_fp):
#     env = {}
#     with open(env_fp, "wb") as fh:
#         pickle.dump(env, fh)

   # add_to_env("LD_LIBRARY_PATH",  "/usr/local/lib/eopenssl11/")
   # add_to_env("LD_LIBRARY_PATH",  f"{project_root}/Builds/Python-3.10.0/")

   # add_to_env("PATH",  f"{project_root}/Builds/Python-3.10.0/bin")
   # add_to_env("PATH",  f"{project_root}/Builds/postgresql-14.0/bin")
