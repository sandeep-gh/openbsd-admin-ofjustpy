# files:
# in /usr/local/lib
# libssl.a
# libcrypto.a
#-I/usr/local/include
#openssl

import os
import sys
from subprocess import Popen, PIPE
from utils import exec_cmd
from config import project_root

exec_cmd(["doas", "cp", "/tmp/libssl.a", "/usr/local/lib"])
exec_cmd(["doas", "cp", "/tmp/libcrypto.a", "/usr/local/lib"])
exec_cmd(["tar", "xvzf", "openssl_inc.tgz"])
exec_cmd(["doas", "cp", "-r", "openssl", "/usr/local/include"])
