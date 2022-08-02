from ClusterShell.NodeSet import NodeSet
from ClusterShell.Task import Task, task_wait
from ClusterShell.Event import EventHandler
import doit

import os
import functools
nodeset = NodeSet()
nodeset.add("192.168.0.105")
#task = task_self()
class MyHandler(EventHandler):

   def ev_read(self, worker, node, sname, msg):
       print(node, msg)

   def ev_hup(self, worker, node, rc):
       if rc != 0:
           print  (f"{node}: returned with error code {rc}")

task = Task()

def check_target(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print ("check_target called")
        targets = kwargs.get('targets')
        print ("targets = ", targets)
        if targets:
            runit = True
            for target in targets:
                runit  = runit and os.path.exists(target)

            if not runit:
                print (f"some targets are missing...running {func}")
                res = func(*args,  **kwargs)
                return res
            else:
                print (f"all target exists..skip {func}")
                return 
                
    return wrapper

def ship_remote_deps(**kwargs):
    remote_deps = kwargs.get('remote_deps')
    if remote_deps:
        for fp in remote_deps:
            print ("ship this please ", fp)
            #basename = os.path.basename(fp)
            #print("basename = ", basename)
            task.copy(f'remotescripts/{fp}', f"/tmp/{fp}", nodes=nodeset , handler=MyHandler())
            task.resume()
            task_wait()

            #TODO: figure out how to generate and capture errors
    
    pass

    
    
# def task_hello():
#     """hello py """
#     @check_target
#     def python_hello(times, text, targets):
#         with open(targets[0], "w") as output:
#             output.write(times * text)
#         pass

#     return {'actions': [(python_hello, [3, "py!\n"])],
#             'targets': ["hello.txt"]
#             }

# def task_compile():
#     return {'actions': ["cc -c main.c"],
#             'file_dep': ["main.c", "defs.h"],
#             'targets': ["main.o"]
#             }

def task_remote_bootstrap():
    @check_target
    def do_action_ok(*args, **kwargs):
        # task remote copy python functio
        # task remote execute
        # task capture output and write to file
        print ("do_action called:", kwargs)
        ship_remote_deps(**kwargs)
        task.shell("cd /tmp; python3 bootstrap.py", nodes=nodeset, handler=MyHandler())
        #task.shell("cd", nodes=nodeset, handler=MyHandler())
        task.resume()
        task_wait()
        targets = kwargs.get('targets')
        #print (targets)
        #res_stderr = list((bytes(msg), nodes) for msg, nodes in task.iter_errors())
        res_stderr = "\n".join(
                str(bytes(msg)) + "=" +   ":".join(nodes) for msg, nodes in task.iter_errors()
                )
        
        if not res_stderr:
            res_stdout = "\n".join(
                str(bytes(msg)) + "=" +   ":".join(nodes) for msg, nodes in task.iter_buffers()
                )
            with open(targets[0], "w+") as fh:
                fh.write(res_stdout)
        else:
            #stop work here things have gone wrong
            with open(targets[0] + ".err", "w+")  as fh:
                fh.write(res_stderr)
                
            return doit.exceptions.TaskFailed("remote_bootstrap failed..see error logs")
        pass

    return {
        'actions': [(do_action_ok, [], {'remote_deps':['bootstrap.py', 'manage_env.py', 'utils.py', 'config.py'],
                                        'targets': ["/tmp/remote_bootstrap.log"],
                                        })],
        }

# def task_setup_ports():
#     def do_action_ok(*args, **kwargs):
#         print ("do_action called:", kwargs)
#         ship_remote_deps(**kwargs)
#         task.shell("cd /tmp; python3 setup_ports.py", nodes=nodeset, handler=MyHandler())
#         #task.shell("cd", nodes=nodeset, handler=MyHandler())
#         task.resume()
#         task_wait()
#         targets = kwargs.get('targets')
#         #print (targets)
#         #res_stderr = list((bytes(msg), nodes) for msg, nodes in task.iter_errors())
#         res_stderr = "\n".join(
#                 str(bytes(msg)) + "=" +   ":".join(nodes) for msg, nodes in task.iter_errors()
#                 )
        
#         if not res_stderr:
#             res_stdout = "\n".join(
#                 str(bytes(msg)) + "=" +   ":".join(nodes) for msg, nodes in task.iter_buffers()
#                 )
#             with open(targets[0], "w+") as fh:
#                 fh.write(res_stdout)
#         else:
#             #stop work here things have gone wrong
#             with open(targets[0] + ".err", "w+")  as fh:
#                 fh.write(res_stderr)
                
#             return doit.exceptions.TaskFailed("remote_bootstrap failed..see error logs")
#         pass

#     return {
#         'actions': [(do_action_ok, [], {'remote_deps':['setup_ports.py', 'utils.py'],
#                                         'targets': ["/tmp/setup_ports.log"],
#                                         })],
#         }


def task_setup_openssl():
    @check_target
    def do_action_ok(*args, **kwargs):
        print ("do_action called:", kwargs)
        ship_remote_deps(**kwargs)
        task.shell("cd /tmp; python3 setup_openssl.py", nodes=nodeset, handler=MyHandler())
        #task.shell("cd", nodes=nodeset, handler=MyHandler())
        task.resume()
        task_wait()
        targets = kwargs.get('targets')
        #print (targets)
        #res_stderr = list((bytes(msg), nodes) for msg, nodes in task.iter_errors())
        res_stderr = "\n".join(
                str(bytes(msg)) + "=" +   ":".join(nodes) for msg, nodes in task.iter_errors()
                )
        
        if not res_stderr:
            res_stdout = "\n".join(
                str(bytes(msg)) + "=" +   ":".join(nodes) for msg, nodes in task.iter_buffers()
                )
            with open(targets[0], "w+") as fh:
                fh.write(res_stdout)
        else:
            #stop work here things have gone wrong
            with open(targets[0] + ".err", "w+")  as fh:
                fh.write(res_stderr)
                
            return doit.exceptions.TaskFailed("remote_bootstrap failed..see error logs")
        pass

    return {
        'actions': [(do_action_ok, [], {'remote_deps':['setup_openssl.py', 'libssl.a', 'libcrypto.a', 'openssl_inc.tgz'],
                                        'targets': ["/tmp/setup_openssl.log"],
                                        })],
        }


def task_buildinstall_python():
    def do_action_ok(*args, **kwargs):
        print ("do_action called:", kwargs)
        ship_remote_deps(**kwargs)
        task.shell("cd /tmp; python3 buildinstall_python.py", nodes=nodeset, handler=MyHandler())
        #task.shell("cd", nodes=nodeset, handler=MyHandler())
        task.resume()
        task_wait()
        targets = kwargs.get('targets')
        #print (targets)
        #res_stderr = list((bytes(msg), nodes) for msg, nodes in task.iter_errors())
        res_stderr = "\n".join(
                str(bytes(msg)) + "=" +   ":".join(nodes) for msg, nodes in task.iter_errors()
                )
        
        if not res_stderr:
            res_stdout = "\n".join(
                str(bytes(msg)) + "=" +   ":".join(nodes) for msg, nodes in task.iter_buffers()
                )
            with open(targets[0], "w+") as fh:
                fh.write(res_stdout)
        else:
            #stop work here things have gone wrong
            with open(targets[0] + ".err", "w+")  as fh:
                fh.write(res_stderr)
                
            return doit.exceptions.TaskFailed("remote_bootstrap failed..see error logs")
        pass

    return {
        'actions': [(do_action_ok, [], {'remote_deps':['buildinstall_python.py'],
                                        'targets': ["/tmp/buildinstall_python.log"],
                                        })],
        }


        
def task_atlast():
    def do_action(targets):
        print ("wrapping up")
        task_wait()
        task.abort()

    return {'actions': [do_action],
            'targets': [],
            }
