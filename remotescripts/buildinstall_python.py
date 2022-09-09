import os
import sys
from subprocess import Popen, PIPE
from utils import exec_cmd
from config import project_root
import os
import wget

CXX = "/usr/bin/c++"


name="Python"
major_version = 3
minor_version = 11
suffix = "0rc1"
sname = f"{name}-{major_version}.{minor_version}"
fqname = f"{sname}.{suffix}"
url = f"https://www.python.org/ftp/python/{major_version}.{minor_version}.0/{fqname}.tar.xz"

print(url)
def buildinstall():
    os.chdir(project_root)
    os.chdir("downloads")
    if not os.path.exists(fqname):
        fn = wget.download(url)
        exec_cmd(["unxz", f"{fqname}.tar.xz"])
        exec_cmd(["tar", "xvf", f"{fqname}.tar"])
        exec_cmd(["rm",  f"{fqname}.tar"])

    os.chdir(fqname)

    #doas pkg_add bzip2 readline sqlite3
    #crypt, libbz2

    build_cmd = f"""CXX={CXX}  OPENSSL_LDFLAGS=-L/usr/local/lib; OPENSSL_LIBS="-lssl -lcrypto"; OPENSSL_INCLUDES=-I/usr/local/include  CFLAGS="-fPIC"   ./configure --prefix={project_root}/Builds/{sname}  --enable-optimizations --with-lto --with-computed-gotos --with-system-ffi  --with-openssl-rpath=auto --with-openssl=/usr/local  --enable-shared
            gmake -j 4
            gmake altinstall
                """
    os.system(build_cmd)

