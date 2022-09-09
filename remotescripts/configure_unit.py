import os
from common_config import project_root
def install():
    install_dir = f"{project_root}/Builds/unit-1.26.0/"
    os.system("""doas useradd -s /usr/local/bin/zsh -p $2b$08$CfofWxG6NNLue9fmT4mThuec7WeJ01C0SrNbKPBjB.bz9UnCexkCG  -L daemon unit""")

    os.chdir(f"{install_dir}")

    if not os.path.exists("/var/run"):
        os.system("doas mkdir /var/run/")
    if not os.path.exists("/var/run/unit"):
        os.system("doas mkdir /var/run/unit")    
    if not os.path.exists("/var/lib"):
        os.system("doas mkdir /var/lib/")
    if not os.path.exists("/var/lib/unit"):
        os.system("doas mkdir /var/lib/unit")
    if not os.path.exists("/var/tmp"):
        os.system("doas mkdir /var/tmp/")
    if not os.path.exists("/var/tmp/unit"):    
        os.system("doas mkdir /var/tmp/unit")
    if not os.path.exists("/var/log/unit"):
        os.system("doas mkdir /var/log/unit")

    os.system(
        "doas chown -R unit:unit /var/run/unit /var/log/unit /var/lib/unit /var/tmp/unit")

if os.path.exists("/tmp/env.sh"):
    install()
