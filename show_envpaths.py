import sys
import pickle
import os

env_fp = "./env.pickle"

def build_env():
    with open(env_fp, "rb") as fh:
        envvars = pickle.load(fh)
        
    env_str = "\n".join(
        [f"""{key}={":".join(envvars[key])}:${key}""" for key in envvars.keys()])
    return env_str

def fix_env():
    with open(env_fp, "rb") as fh:
        envvars = pickle.load(fh)

    envvars.pop("PYTHONPATH", None)
    
    env_str = "\n".join(
        [f"""{key}={":".join(envvars[key])}:${key}""" for key in envvars.keys()])
    print (env_str)
    with open(env_fp, "wb") as fh:
        pickle.dump(envvars, fh)
        
#fix_env()
print (build_env())
