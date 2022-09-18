import os
import sys
import subprocess
#from common_config import project_root
#from common_utils import exec_cmd
from config import project_root
from utils import exec_cmd

def delete_site(site_name="example", site_domain=".in"):
    exec_cmd(
        f"""doas rm -rf    /var/www/htdocs/{site_name}{site_domain}  /etc/nginx/conf.d/{site_name}{site_domain}.conf""".split()
    )


def host_site(content_tgz_fn, applabel, site_name, site_domain, port):
    # the port at which nginx and unit communicate
    # to be replace with unix socket 
    nginx_unit_port = port + 80
    
    nginx_site_directive = f"""

    upstream {applabel}_unit {{
    # fail_timeout=0 means we always retry an upstream even if it failed
    server 127.0.0.1:{nginx_unit_port} fail_timeout=0;

    }}
    server {{
    listen         {port}; 
    listen         [::]:{port}; 
    server_name    {site_name}{site_domain} www.{site_name}{site_domain};
    root           /var/www/htdocs/{site_name}{site_domain};
    location / {{
    proxy_pass http://{applabel}_unit;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;


    }}
    }}"""

    #TODO: why we need try_files
    #index          index.html;
    #try_files $uri /index.html;
    
    try:
        res = exec_cmd(
            f"mkdir /tmp/{site_name}{site_domain}".split())
        os.chdir(f"/tmp/{site_name}{site_domain}")
        res = exec_cmd(
            f"tar xvzf /tmp/{content_tgz_fn}".split())

        # os.chdir(f"/var/www/htdocs/{site_name}{site_domain}")
        cmdl = f"""doas  mv /tmp/{site_name}{site_domain}  /var/www/htdocs/ """.split(
        )
        # Already did that 
        exec_cmd(cmdl)

        # ============================= done =============================
        with open(f"/tmp/{site_name}{site_domain}.conf", "w") as fh:
            fh.write(nginx_site_directive)

        cmdl = ["doas", "cp", f"/tmp/{site_name}{site_domain}.conf",
                "/etc/nginx/conf.d/"]
        
        exec_cmd(cmdl)

        #configure a listener in Unit

        # first build a virtual env
        os.system(f"""doas sh /tmp/setup_py_venv.sh {site_name} {site_domain}"""
                  )
        
        # This one works 
        #     {
        #             "listeners": {
        #                 "*:8080": {
        #                     "pass": "routes"
        #                 }
        #             },

        #             "routes": [
        #                 {
        #                     "action": {
        #                         "pass": "applications/starlette"
        #                     }
        #                 }
        #             ],

        #             "applications": {
        #                 "starlette": {
        #                     "type": "python 3.11",
        #                     "path": "/var/www/htdocs/monallabs.in/",
        #                     "home": "/var/www/htdocs/monallabs.in/venv/",
        #                     "module": "simpleapp",
        #                     "callable": "app"
        #                 }
        #             }
        # }
                  
        unit_directive = f"""

        {{
            "listeners": {{
                "*:{nginx_unit_port}": {{
                    "pass": "routes"
                }}
            }},

            "routes": [
                {{
                    "action": {{
                        "pass": "applications/starlette"
                    }}
                }}
            ],

            "applications": {{
                "starlette": {{
                    "type": "python 3.11",
                    "path": "/var/www/htdocs/{site_name}{site_domain}/",
                    "home": "/var/www/htdocs/{site_name}{site_domain}/venv/",
                    "module": "{applabel}",
                    "callable": "app"
                }}
            }}
        }}

        """
        with open("/tmp/unit_cfg.json", "w") as fh:
            fh.write(unit_directive)


def deploy(content_tgz_fn, applabel, site_name, site_domain, port=9000):
    #delete_site()
    #see /home/shared/deploymentdata/example.tgz
    #
    host_site(content_tgz_fn, applabel, site_name, site_domain, port=9000)
    # start nginx
    os.system("doas /usr/sbin/nginx -s reload&")


# if os.path.exists("/tmp/env.sh"):
#     install()

