export LD_LIBRARY_PATH=/home/shared/Builds/Python-3.11/lib:/home/shared/Builds/unit-1.27.0/lib:$LD_LIBRARY_PATH
export PATH=/home/shared/Builds/Python-3.11/bin:/home/shared/Builds/unit-1.27.0/sbin/:$PATH
cd /var/www/htdocs/$1$2
python3.11 -m venv venv
. ./venv/bin/activate
pip3  install starlette[full]
deactivate

