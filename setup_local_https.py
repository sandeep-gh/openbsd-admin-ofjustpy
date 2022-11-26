deployment_machine=192.168.0.105
development_machine=192.168.0.102
browser_machine=192.168.0.107
browser_sudo_user = "pi"

passphrase = "memorable"

src_dir = os.path.dirname(os.path.realpath(__file__))
# Step 1: copy passphrase.txt and setup_local_https_deploy_machine.py"
nodeset = NodeSet()
nodeset.add(deployment_machine)
task.copy(f"{src_dir}/passphrase.txt", "/tmp", nodes=nodeset)
task.copy(f"{src_dir}/setup_local_https_deploy_machine.py", "/tmp", nodes=nodeset)
# generate myCA.key and myCA.pem
task.shell("cd /tmp/; python3 setup_local_https_deploy_machine.py", nodes=nodeset)


# ----------------------------------- Done Step 1 --------------------

# Step 2: Copy generated certs from deploy to local/development machine
nodeset = NodeSet()
nodeset.add(development_machine)
task.rcopy(f"/tmp/certs/myCA.key", "/tmp", nodes=nodeset)
task.rcopy(f"/tmp/certs/myCA.pem", "/tmp", nodes=nodeset)

# ----------------------------------- Done Step 2 --------------------

# Step 3: move the keys from local/devel machine to browser machine
# TODO: use pi or a user with sudo privileges 
nodeset = NodeSet()
nodeset.add(browser_machine)
task.copy(f"/tmp/myCA.key", "/tmp", nodes=nodeset)
task.copy(f"/tmp/myCA.pem", "/tmp/myCA.crt", nodes=nodeset)
#TODO: Also ship passphrase.txt file
task.shell("sudo cp /tmp/myCA.pem /usr/local/share/ca-certificates", nodes=nodeset)
task.shell("sudo update-ca-certificates", nodes=nodeset)


# ----------------------------------- Done Step 2 --------------------


# Step 3: Now that we are a  CA on the device; lets sign some certificates
# for any dev sites




#-------------- Done step 3---------------

#Step 4; add site certificate and keys to nginx

cp monallabs.test.key monallabs.test.crt ~/bsd102/certs_for_local_https/

