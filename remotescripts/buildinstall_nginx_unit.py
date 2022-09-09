#TODO: what about process isolation

#proj, gdal, geos, tiff, protobuf, readline
#dependency: iconv

import importlib
import os
import time

import subprocess
import wget
from utils import exec_cmd
from config import project_root


CXX = "/usr/bin/c++"

os.chdir(project_root)
if not os.path.exists("downloads"):
    os.makedirs("downloads")


version = "1.27.0"
name = "unit"
geturl = f"https://unit.nginx.org/download/{name}-{version}.tar.gz"


def install(force_rebuild=False):
    os.chdir("downloads")

    if not os.path.exists(f"{name}-{version}"):
        fn = wget.download(geturl)
        print(fn)
        os.system(f"gunzip {name}-{version}.tar.gz")
        os.system(f"tar xvf {name}-{version}.tar")

    try:
        os.chdir(f"{project_root}/Builds/")
        if not os.path.exists(f"{name}-{version}") or force_rebuild:
            os.makedirs(f"{name}-{version}")
            os.chdir(f"{project_root}/downloads/{name}-{version}")
            build_cmd = f""". /tmp/env.sh;
            ./configure --prefix=/home/shared/Builds/{name}-{version}  --openssl  --user=www --group=www --ld-opt="-L/usr/local/lib/ -Wl,-rpath /usr/local/lib/ -lssl -lcrypto"  --cc-opt="-fPIC -I/usr/local/include/ --debug";
            . /tmp/env.sh; . /home/shared/pyvenv/bin/activate; 
            ./configure  python  --lib-path={project_root}/Builds/Python-3.11/lib  --config=/home/shared/Builds/Python-3.11/bin/python3.11-config
            make 
            make install

            """
            os.system(build_cmd)

    except Exception as e:
        print(e)
        os.chdir(f"{project_root}")
        os.rmdir(f"Builds/{name}-{version}")


# os.chdir(f"{project_root}")
def buildinstall():
    if os.path.exists("/tmp/env.sh"):
        install()
