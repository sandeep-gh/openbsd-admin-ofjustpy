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
    nginx_unit_port = int(port) + 80

    # this works and works well so far. but everything gets passed to starlette -- no static part

    nginx_site_directive = f"""
    upstream {applabel}_unit {{
    # fail_timeout=0 means we always retry an upstream even if it failed
    server 127.0.0.1:{nginx_unit_port} fail_timeout=0;

    }}

    server {{
    listen         443 ssl;
    ssl_certificate /etc/nginx/conf.d/monallabs.test.crt;
    ssl_certificate_key /etc/nginx/conf.d/monallabs.test.key;
    location / {{
         proxy_pass http://{applabel}_unit;
         proxy_http_version 1.1;
         proxy_set_header Upgrade $http_upgrade;
         proxy_set_header Connection "Upgrade";
         proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header        X-Forwarded-Proto $scheme;
     proxy_read_timeout 999999999;

    }}

    }}
    """
    
    
    # nginx_site_directive = f"""
    
    # upstream {applabel}_unit {{
    # # fail_timeout=0 means we always retry an upstream even if it failed
    # server 127.0.0.1:{nginx_unit_port} fail_timeout=0;

    # }}
    # server {{
    # listen         {port}; 
    # listen         [::]:{port}; 
    # server_name    {site_name}{site_domain} www.{site_name}{site_domain};
    # root           /var/www/htdocs/{site_name}{site_domain};
    
    # location / {{
    # proxy_pass http://{applabel}_unit;
    # proxy_set_header Host $host;
    # proxy_set_header X-Real-IP $remote_addr;
    
    
    # }}
    # }}

    # server {{
    # listen         443 ssl;
    # ssl_certificate /etc/nginx/conf.d/monallabs.test.crt;
    # ssl_certificate_key /etc/nginx/conf.d/monallabs.test.key;
    # location / {{
    # proxy_pass http://{site_name}{site_domain}:{port}/;
    # proxy_read_timeout {port};
    # }}
    # }}
    # """

    #TODO: why we need try_files
    #index          index.html;
    #try_files $uri /index.html;
    
    try:
        res = exec_cmd(
            f"mkdir /tmp/{site_name}{site_domain}".split())
        os.chdir(f"/tmp/{site_name}{site_domain}")
        res = exec_cmd(
            f"tar xvzf /tmp/{content_tgz_fn}".split())

        
        cmdl = f"""doas  mv /tmp/{site_name}{site_domain}  /var/www/htdocs/ """.split(
        )
        # Already did that 
        exec_cmd(cmdl)
        os.chdir(f"/var/www/htdocs/{site_name}{site_domain}")
        os.system("""
        cp -r tailwind-tags-main/tailwind_tags/ monalwebworks.in/
        cp -r ofjustpy-react-main/ofjustpy_react monalwebworks.in/
        cp -r ofjustpy-main/ofjustpy/ monalwebworks.in/
        cp addict-master/addict/  monalwebworks.in/
        cp -r justpy-replace_vue_with_svelte/jpcore/ monalwebworks.in/
        cp -r justpy-replace_vue_with_svelte/justpy/ monalwebworks.in/
        """)
        


        TODO: copy over certificate and keys

        
        ============================= done =============================
        with open(f"/tmp/{site_name}{site_domain}.conf", "w") as fh:
            fh.write(nginx_site_directive)

        cmdl = ["doas", "cp", f"/tmp/{site_name}{site_domain}.conf",
                "/etc/nginx/conf.d/"]
        
        exec_cmd(cmdl)

        cmdl = f"""doas  mv /tmp/{site_name}.test.crt  /etc/nginx/conf.d """.split(
        )

        exec_cmd(cmdl)

        cmdl = f"""doas  mv /tmp/{site_name}.test.key  /etc/nginx/conf.d """.split(
        )

        exec_cmd(cmdl)

        

        #configure a listener in Unit

        # first build a virtual env
        os.system(f"""doas sh /tmp/setup_py_venv.sh {site_name} {site_domain}"""
                  )
        
                  
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

        os.system("""doas curl -X PUT --data-binary @/tmp/unit_cfg.json --unix-socket  /var/run/unit/control.sock http://localhost/config/""")

        
    except Exception as e:
        print ("Ran into error ", e)
        pass
    
def deploy(content_tgz_fn, applabel, site_name, site_domain, port):
    #delete_site()
    #see /home/shared/deploymentdata/example.tgz
    #
    host_site(content_tgz_fn, applabel, site_name, site_domain, port)
    # start nginx
    #os.system("doas /usr/sbin/nginx -s reload&")


# if os.path.exists("/tmp/env.sh"):
#     install()

