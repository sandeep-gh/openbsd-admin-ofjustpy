import os
from utils import append_to_file
if not os.path.exists("/usr/ports"):

    get_ports = """
    cd /tmp
    ftp https://cdn.openbsd.org/pub/OpenBSD/$(uname -r)/{ports.tar.gz,SHA256.sig}
    signify -Cp /etc/signify/openbsd-$(uname -r | cut -c 1,3)-base.pub -x SHA256.sig ports.tar.gz
    cd /usr
    doas tar xzf /tmp/ports.tar.gz
    """
    os.system(get_ports)

    doasconf = open("/etc/doas.conf", "r").read()
    precondition = 'adming as _pbuild' in doasconf
    print ("precondition = ", precondition)
    if not precondition:
        append_to_file("/etc/doas.conf",
                       """permit keepenv nopass adming as _pbuild \n
permit keepenv nopass adming as _pfetch \n
permit keepenv nopass adming as root \n
""")
        append_to_file("/etc/mk.conf",
                       """WRKOBJDIR=/usr/local/ports/pobj/
    DISTDIR=/usr/ports/distfiles
    PACKAGE_REPOSITORY=/usr/ports/packages
    PORTS_PRIVSEP=yes
    SUDO=doas
    """)



    setup_ports = """
    doas usermod -G _pbuild adming
    doas chown -R _pbuild:_pbuild /usr/ports 
    doas mkdir /usr/ports/distfiles
    doas mkdir /usr/ports/packages                     
    doas mkdir /usr/ports/plist    
    doas mkdir /usr/ports/pobj  
    doas mkdir /usr/ports/pbulk
    doas mkdir /usr/local/ports
    doas chown _pbuild:wheel /usr/local/ports


    doas chown -R _pbuild:_pbuild /usr/ports/{packages,plist,pobj,pbulk}
    doas chown -R _pfetch:_pfetch /usr/ports/distfiles
    doas install -d -o _pfetch -g _pfetch /usr/ports/distfiles
    doas install -d -o _pbuild -g _pbuild /usr/ports/{packages,plist,pobj,pbulk}
    doas pkg_add portslist
    """
    os.system(setup_ports)
else:
    print("ports already is setup")

    
