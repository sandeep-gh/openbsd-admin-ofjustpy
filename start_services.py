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

task.copy("/tmp/env.sh", "/tmp", nodes=nodeset)
task.resume()
task_wait()


task.copy("/home/kabira/Development/openbsd-admin-ofjustpy/remotescripts/start_services.py", "/tmp", nodes=nodeset)
task.resume()
task_wait()

task.copy("/home/kabira/Development/openbsd-admin-ofjustpy/remotescripts/start_unitd.sh", "/tmp", nodes=nodeset)
task.resume()
task_wait()


task.shell("cd /tmp; python3 start_services.py", nodes=nodeset, handler=MyHandler())
task.resume()
task_wait()
task.abort()
