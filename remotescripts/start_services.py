import os
import psutil
#from deploymentscripts import manage_env
def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

if not checkIfProcessRunning("nginx"):
    os.system(". /tmp/env.sh; .  /home/shared/pyvenv/bin/activate; doas /usr/sbin/nginx &")
    #os.system("curl example.in")


if not checkIfProcessRunning("unitd"):
    install_dir="/home/shared/Builds/unit-1.27.0/" #TODO: grab it from install file

    # os.system(
    #         f". /tmp/env.sh; . /home/shared/pyvenv/bin/activate; doas {install_dir}/sbin/unitd --control unix:/var/run/unit/control.sock  --pid /var/run/unit.pid --log /var/log/unit/unit.log --modules {install_dir}/modules --state /var/lib/unit/ --tmp /var/tmp/unit/")
    os.system(f"cd /tmp; doas sh start_unitd.sh {install_dir}")

    
