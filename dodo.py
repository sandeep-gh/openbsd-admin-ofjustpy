from ClusterShell.NodeSet import NodeSet
from ClusterShell.Task import Task, task_wait
from ClusterShell.Event import EventHandler
import doit
import importlib
import os
import functools
from remotescripts import config
import pickle

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
    pass


def check_target(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        targets = kwargs.get('targets')

        if targets:
            runit = True
            for target in targets:
                runit  = runit and os.path.exists(target)

            if not runit:
                print (f"some targets are missing...running {func}")
                #ship the dependencies
                ship_remote_deps(**kwargs)
                res = func(*args,  **kwargs)
                targets = kwargs.get('targets')
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
        

            else:
                print (f"all target exists..skip {func}")
                return 
                
    return wrapper


def task_setup_env():
    def do_action(*args, **kwargs):
        # initialize the env bookkeeping
        env_fp = "env.pickle"
        if not os.path.exists(env_fp):
            env = {}
            with open(env_fp, "wb") as fh:
                pickle.dump(env, fh)

        

        

def task_remote_bootstrap():
    @check_target
    def do_action_ok(*args, **kwargs):
        task.shell("cd /tmp; python3 bootstrap.py", nodes=nodeset, handler=MyHandler())
        task.resume()
        task_wait()

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
        task.shell("cd /tmp; python3 setup_openssl.py", nodes=nodeset, handler=MyHandler())
        #task.shell("cd", nodes=nodeset, handler=MyHandler())
        task.resume()
        task_wait()
        
        pass

    return {
        'actions': [(do_action_ok, [], {'remote_deps':['setup_openssl.py', 'libssl.a', 'libcrypto.a', 'openssl_inc.tgz'],
                                        'targets': ["/tmp/setup_openssl.log"],
                                        })],
        }


def task_buildinstall_python():
    @check_target
    def do_action_ok(*args, **kwargs):
        task.shell("""cd /tmp; python3 -c "import buildinstall_python; buildinstall_python.buildinstall()""", nodes=nodeset, handler=MyHandler())
        task.resume()
        task_wait()
        pass

    return {
        'actions': [(do_action_ok, [], {'remote_deps':['buildinstall_python.py'],
                                        'targets': ["/tmp/buildinstall_python.log"],
                                        })],
        }

def load_module(modname):
    spec = importlib.util.spec_from_file_location(modname, f"./remotescripts/{modname}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
    
def task_pyenv():
    def do_action(*args, **kwargs):
        print ("only this should be called")
        mod = load_module("buildinstall_python")
        basepath = f"{config.project_root}/Builds/{mod.sname}"
        
        print (path)
        pass
    return {
        'actions': [do_action]
        }
        
def task_atlast():
    def do_action(targets):
        print ("wrapping up")
        task_wait()
        task.abort()

    return {'actions': [do_action],
            'targets': [],
            }
