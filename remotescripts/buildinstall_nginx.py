import os
import sys
from subprocess import Popen, PIPE
from utils import exec_cmd
from config import project_root
import os
import wget

CXX = "/usr/bin/c++"

os.chdir(project_root)

name="nginx"
version="1.23.1"
fqname=f"{name}-{version}"
url = "http://nginx.org/download/{fqn}.tar.gz"


def openssl():
    version = "1.1.1q"
    name = "openssl"
    url = "https://www.openssl.org/source/openssl-1.1.1q.tar.gz"
    os.chdir("downloads")
    if not os.path.exists(f"{name}-{version}"):
        fn = wget.download(url)
        os.system(f"gunzip {name}-{version}.tar.gz")
        os.system(f"tar xvf {name}-{version}.tar")
    os.chdir(project_root)

def install(force_rebuild=False):
    openssl()
    os.chdir("downloads")

    if not os.path.exists(fqname):
        fn = wget.download(url)
        os.system(f"gunzip {name}-{version}.tar.gz")
        os.system(f"tar xvf {name}-{version}.tar")

    try:
        os.chdir(f"{project_root}/Builds/")
        if not os.path.exists(f"{name}-{version}"):
            os.makedirs(f"{name}-{version}")
            os.chdir(f"{project_root}/downloads/{name}-{version}")
            build_cmd = f""". /tmp/env.sh ;
            ./configure --prefix={project_root}/Builds/{name}-{version} \
            --sbin-path=/usr/sbin/nginx \
            --modules-path=/usr/lib64/nginx/modules  \
            --conf-path=/etc/nginx/nginx.conf \
            --error-log-path=/var/log/nginx/error.log \
            --http-log-path=/var/log/nginx/access.log \
            --pid-path=/var/run/nginx.pid \
            --lock-path=/var/run/nginx.lock \
            --http-client-body-temp-path=/var/cache/nginx/client_temp \
            --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
            --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
            --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
            --http-scgi-temp-path=/var/cache/nginx/scgi_temp \
            --user=www \
            --group=www   \
            --with-compat \
            --with-threads \
            --with-http_addition_module \
            --with-http_auth_request_module \
            --with-http_dav_module \
            --with-http_flv_module \
            --with-http_gunzip_module \
            --with-http_gzip_static_module \
            --with-http_mp4_module \
            --with-http_random_index_module \
            --with-http_realip_module \
            --with-http_secure_link_module \
            --with-http_slice_module \
            --with-http_ssl_module \
            --with-http_stub_status_module \
            --with-http_sub_module \
            --with-http_v2_module \
            --with-mail \
            --with-mail_ssl_module \
            --with-stream \
            --with-stream_realip_module \
            --with-stream_ssl_module \
            --with-stream_ssl_preread_module \
            --with-openssl=/home/shared/downloads/openssl-1.1.1l/
            
            make
            doas make install
            """
            print(build_cmd)
            os.system(build_cmd)

            # ==================== path ownerships ===================
            # /var/log/nginx
            # /var/run/nginx
            # /var/run/nginx.pid
            # =============================== done ===============================
    except Exception as e:
        print(e)
        os.chdir(f"{project_root}")
        os.rmdir(f"Builds/{name}-{version}")


# os.chdir(f"{project_root}")

if os.path.exists("/tmp/env.sh"):
    print ("installing..")
    install()
    
