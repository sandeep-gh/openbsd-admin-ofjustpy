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

print(build_env())
