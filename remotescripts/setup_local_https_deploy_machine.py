import os
from utils import exec_cmd
os.system("""
mkdir /tmp/certs;
/tmp/certs;
openssl genrsa -des3 -out myCA.key -passout file:/tmp/passphrase.txt 2048
openssl req -x509 -new -nodes -key myCA.key -sha256 -days 1825 -passin file:/tmp/passphrase.txt   -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=www.example.com"  -out myCA.pem
"""
    )

task.shell("openssl genrsa -out monallabs.test.key 2048", nodes=nodeset)
task.shell("""openssl req    -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=www.example.com" -new -key monallabs.test.key -out monallabs.test.csr""")


task.copy("monallabs.test.ext", /tmp/, nodes=nodeset)
# final command

task.shell("openssl x509 -req -in monallabs.test.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -passin file:/tmp/passphrase.txt -out monallabs.test.crt -days 825 -sha256 -extfile monallabs.test.ext")



# TODO: modify nginx
