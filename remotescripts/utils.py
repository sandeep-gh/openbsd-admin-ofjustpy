import os
import sys
from subprocess import Popen, PIPE

def exec_cmd(cmdl):
    process = Popen(cmdl, stdout=PIPE, stderr=PIPE)
    output, err = process.communicate()
    print(output, file=sys.stdout)
    print(err, file=sys.stderr)

def append_to_file(fullfp:str, apstr:str, owner="adming"):
    dirn = os.path.dirname(fullfp)
    fn = os.path.basename(fullfp)
    if os.path.exists(fullfp):
        os.system(f"doas cp {fullfp} {fullfp}.premod")
        os.system(f"cp {fullfp} /tmp/{fn}")
        
    with open(f"/tmp/{fn}", "a") as fh:
        fh.write(apstr)
    os.system(f"doas mv /tmp/{fn} {fullfp}")
    os.system(f"doas {owner}:{owner} {fullfp}")
              
    
