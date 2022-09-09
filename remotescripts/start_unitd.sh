install_dir=$1
. /tmp/env.sh
. /home/shared/pyvenv/bin/activate
${install_dir}/sbin/unitd --control unix:/var/run/unit/control.sock  --pid /var/run/unit.pid --log /var/log/unit/unit.log --modules ${install_dir}/modules --state /var/lib/unit/ --tmp /var/tmp/unit/
