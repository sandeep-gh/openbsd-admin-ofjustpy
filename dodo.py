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
print ("current working dir = ", os.getcwd())
#task = task_self()
class MyHandler(EventHandler):

   def ev_read(self, worker, node, sname, msg):
       print(node, msg)

   def ev_hup(self, worker, node, rc):
       if rc != 0:
           print  (f"{node}: returned with error code {rc}")

task = Task()

env_fp = initial_workdir + "/env.pickle"

def build_env():
    with open(env_fp, "rb") as fh:
        envvars = pickle.load(fh)
    env_str = "\n".join(
        [f"""export {key}={":".join(envvars[key])}:${key}""" for key in envvars.keys()])
    return env_str
 
def add_to_env(varname, path):
    with open(env_fp, "rb") as fh:
        envvars = pickle.load(fh)

    if varname in envvars.keys():
        if path not in envvars[varname]:
            envvars[varname].append(path)
    else:
        envvars[varname] = []
        envvars[varname].append(path)
    print(envvars)
    with open(env_fp, "wb") as fh:
        pickle.dump(envvars, fh)

        
def exec_clush_cmd(cmdargl):
    """
    cmdargl: clush command argument as a list
    """
    res = subprocess.check_output(["clush", "-w", target_node,  *cmdargl])
    # in case you don't like the output
    # https://stackoverflow.com/questions/42965689/replacing-a-text-with-n-in-it-with-a-real-n-output
    #formatted_output = res.replace('\\n', '\n').replace('\\t', '\t')
    return res.decode("utf-8")

 
def ship_remote_deps(*remote_deps):
   print ("in ship remote_deps = ", remote_deps)
   for fp in remote_deps:
      print ("ship this please ", fp)
      task.copy(fp, "/tmp/", nodes=nodeset , handler=MyHandler())
      task.resume()
      task_wait()
      print("-==============DONE==================")
      print(fp)
      print("-==============DONE==================")


def check_target(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        targets = kwargs.get('targets')

        if targets:
            runit = True
            for target in targets:
               #print ("current working dir = ", os.getcwd())
               #print ("now checking target = ", initial_workdir + target, " ", os.path.exists(initial_workdir + target))
               flag = os.path.exists(initial_workdir + target)
               runit  = runit and flag
               #print ("now checking runit = ", runit)

            if not runit:
                print (f"some targets are missing...running {func}")
                #update env variables 
                with open("/tmp/env.sh", "w") as fh:
                   fh.write(build_env())
        
                #ship the dependencies
                remote_deps = kwargs.get('remote_deps')
                ship_remote_deps(
                   *[f'remotescripts/{_}' for _ in [*remote_deps, "utils.py", "config.py" ]],
                   "/tmp/env.sh"
                   
                    )
                res = func(*args,  **kwargs)
                targets = kwargs.get('targets')
                res_stderr = "\n".join(
                    str(bytes(msg)) + "=" +   ":".join(nodes) for msg, nodes in task.iter_errors()
                )
        
                if not res_stderr:
                    res_stdout = "\n".join(
                        str(bytes(msg)) + "=" +   ":".join(nodes) for msg, nodes in task.iter_buffers()
                    )
                    with open(initial_workdir + targets[0], "w+") as fh:
                        fh.write(res_stdout)
                else:
                    #stop work here things have gone wrong
                    with open(initial_workdir + targets[0] + ".err", "w+")  as fh:
                        fh.write(res_stderr)
                
                    return doit.exceptions.TaskFailed("remote_bootstrap failed..see error logs")
        

            else:
                print (f"all target exists..skip {func}")
                return 
                
    return wrapper



print ("env_fp = ", env_fp)
def task_setup_env():
    def do_action(*args, **kwargs):
        # initialize the env bookkeeping
        if not os.path.exists(env_fp):
            env = {}
            with open(env_fp, "wb") as fh:
                pickle.dump(env, fh)

    return {
        'actions': [(do_action, [], {'remote_deps':[],
                                     'file_dep' : [env_fp],
                                        'targets': [env_fp],
                                        })],
        }

        

def task_remote_bootstrap():
    @check_target
    def do_action_ok(*args, **kwargs):
        task.shell("cd /tmp; python3 bootstrap.py", nodes=nodeset, handler=MyHandler())
        task.resume()
        task_wait()

        pass

    return {
        'actions': [(do_action_ok, [], {'remote_deps':['bootstrap.py', 'manage_env.py', 'utils.py', 'config.py'],
                                        'targets': ["/logs/remote_bootstrap.log"],
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
                                        'targets': ["/logs/setup_openssl.log"],
                                        })],
        }


def task_buildinstall_python():
    @check_target
    def do_action_ok(*args, **kwargs):
        task.shell("""
        cd /tmp; python3 -c "import buildinstall_python; buildinstall_python.buildinstall()"
        """, nodes=nodeset, handler=MyHandler())
        task.resume()
        task_wait()
        mod = load_module("buildinstall_python")
        basepath = f"{config.project_root}/Builds/{mod.sname}"
        add_to_env("LD_LIBRARY_PATH", f"{basepath}/lib")
        add_to_env("PATH", f"{basepath}/bin")
        pass

    return {
        'actions': [(do_action_ok, [], {'remote_deps':["buildinstall_python.py"],
                                        'targets': ["/logs/buildinstall_python.log"],
                                        })],
        }


# def task_setup_python():
#    """
#    - create virtual env
#     - pip install weget 
#    - 
#    """
#    def do_action(*args, **kwargs):
#       task.shell("""
#         cd /tmp; python3 -c "import setup_python; setup_python.setup()"
#         """, nodes=nodeset, handler=MyHandler())
#       task.resume()
#       task_wait()
        
def task_buildinstall_nginx():
    @check_target
    def do_action_ok(*args, **kwargs):
        task.shell("""
        cd /tmp; . /tmp/env.sh; source  /home/shared/pyvenv/bin/activate;  python3 -c "import buildinstall_nginx; buildinstall_nginx.buildinstall()"
        """, nodes=nodeset, handler=MyHandler())
        task.resume()
        task_wait()
        # No need to add any path;
        # everything is installed in /usr/sbin, /etc, /var
        # mod = load_module("buildinstall_nginx")
        # basepath = f"{config.project_root}/Builds/{mod.sname}"
        # add_to_env("LD_LIBRARY_PATH", f"{path}/lib")
        # add_to_env("PATH", f"{path}")

        # add_to_env("LD_LIBRARY_PATH", f"{basepath}/lib")
        # add_to_env("PATH", f"{basepath}/bin")
        pass

    return {
        'actions': [(do_action_ok, [], {'remote_deps':["buildinstall_nginx.py"],
                                        'targets': ["/logs/buildinstall_nginx.log"],
                                        'pkgs': ['pcre']
                                        })],
        }

def task_buildinstall_nginx_unit():
    @check_target
    def do_action_ok(*args, **kwargs):
        task.shell("""cd /tmp; 
         python3 -c "import buildinstall_nginx_unit; buildinstall_nginx_unit.buildinstall()"
        """, nodes=nodeset, handler=MyHandler())
        task.resume()
        task_wait()
        # No need to add any path;
        # everything is installed in /usr/sbin, /etc, /var
        mod = load_module("buildinstall_nginx_unit")
        path = f"{config.project_root}/Builds/{mod.name}-{mod.version}"
        add_to_env("LD_LIBRARY_PATH", f"{path}/lib")
        add_to_env("PATH", f"{path}/sbin/")
        # basepath = f"{config.project_root}/Builds/{mod.sname}"
        # add_to_env("LD_LIBRARY_PATH", f"{path}/lib")
        # add_to_env("PATH", f"{path}")

        # add_to_env("LD_LIBRARY_PATH", f"{basepath}/lib")
        # add_to_env("PATH", f"{basepath}/bin")
        pass

    return {
        'actions': [(do_action_ok, [], {'remote_deps':["buildinstall_nginx_unit.py", "nginx.conf"],
                                        'targets': ["/logs/buildinstall_nginx_unit.log"],
                                        'pkgs': ['pcre']
                                        })],
        } 

 
def load_module(modname):

    spec = importlib.util.spec_from_file_location(modname, f"./remotescripts/{modname}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
    
# def task_pyenv():
#     def do_action(*args, **kwargs):
#         print ("only this should be called")
#         try:
#            mod = load_module("buildinstall_python")
#            basepath = f"{config.project_root}/Builds/{mod.sname}"
#            print("basepath = ", basepath)
#         except Exception as e:
#            print ("ran into erro ", e)
#            print ("need to suppress so that task can exit gracefully")
        
        
#         pass
#     return {
#         'actions': [do_action]
#         }
        
def task_atlast():
    def do_action(targets):
        print ("wrapping up")
        task_wait()
        task.abort()

    return {'actions': [do_action],
            'targets': [],
            }
 
