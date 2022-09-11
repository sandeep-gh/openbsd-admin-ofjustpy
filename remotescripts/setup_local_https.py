import os
from utils import exec_cmd

exec_cmd("mkdir /tmp/certs")
os.chdir("/tmp/certs")
# create pem
#openssl genrsa -des3 -out myCA.key 2048
#openssl req -x509 -new -nodes -key myCA.key -sha256 -days 1825 -out myCA.pem

# from browser device


#=======================

#pass phrase memorable


# openssl genrsa -out monallabs.test.key 2048
# openssl req -new -key monallabs.test.key -out monallabs.test.csr

#on dev machine
# openssl genrsa -out monallabs.test.key 2048
# openssl req -new -key monallabs.test.key -out monallabs.test.csr

# monallabs.test.ext
# authorityKeyIdentifier=keyid,issuer
# basicConstraints=CA:FALSE
# keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
# subjectAltName = @alt_names

# [alt_names]
# DNS.1 = monallabs.test


openssl x509 -req -in monallabs.test.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out monallabs.test.crt -days 825 -sha256 -extfile monallabs.test.ext
