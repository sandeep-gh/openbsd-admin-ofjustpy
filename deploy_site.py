from ClusterShell.NodeSet import NodeSet
from ClusterShell.Task import Task, task_wait
from ClusterShell.Event import EventHandler
import doit
import importlib
import os
import functools
from remotescripts import config
import pickle
import sys
import subprocess

target_node = "192.168.0.105"
src_dir = os.path.dirname(os.path.realpath(__file__))
nodeset = NodeSet()
nodeset.add(target_node)
initial_workdir = doit.get_initial_workdir() 
class MyHandler(EventHandler):

   def ev_read(self, worker, node, sname, msg):
       print(node, msg)

   def ev_hup(self, worker, node, rc):
       if rc != 0:
           print  (f"{node}: returned with error code {rc}")
           raise ValueError("Remote operation failed: ")


task = Task()

def deploy_site(content_tgz_fp, applabel, site_name, site_domain):
    task.copy(content_tgz_fp, "/tmp", nodes=nodeset, handler=MyHandler())
    task.resume()
    task_wait()

    task.copy(f"{src_dir}/remotescripts/deploy_site.py", "/tmp", nodes=nodeset, handler=MyHandler())
    task.resume()
    task_wait()

    content_tgz_fn = os.path.basename(content_tgz_fp)
    task.shell(f"""
        cd /tmp; python3 -c "import deploy_site; deploy_site.deploy(\\"{content_tgz_fn}\\", \\"{applabel}\\", \\"{site_name}\\", \\"{site_domain}\\")"
        """, nodes=nodeset, handler=MyHandler())

    task.resume()
    task_wait()
    task.abort()


import sys
deploy_site(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
