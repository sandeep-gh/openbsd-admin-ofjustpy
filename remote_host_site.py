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
sys.path.insert(1, "./remotescripts")
nodeset = NodeSet()
nodeset.add(target_node)
initial_workdir = doit.get_initial_workdir()

class MyHandler(EventHandler):

   def ev_read(self, worker, node, sname, msg):
       print(node, msg)

   def ev_hup(self, worker, node, rc):
       if rc != 0:
           print  (f"{node}: returned with error code {rc}")

           
task = Task()
