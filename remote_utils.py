import os
import sys
from subprocess import Popen, PIPE

def exec_cmd(cmdl):
    process = Popen(cmdl, stdout=PIPE, stderr=PIPE)
    output, err = process.communicate()
    print(output, file=sys.stdout)
    print(err, file=sys.stderr)
