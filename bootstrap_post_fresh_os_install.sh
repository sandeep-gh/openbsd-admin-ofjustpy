adpass=`encrypt -p`
useradd -m -L staff -p \"$adpass\" -G wheel adming
usermod -G wheel adming
echo "permit nopass :wheel" >>/etc/doas.conf
pkg_add -uvi
su adming -c "doas pkg_add python3; groupadd -g 1002 shared"
su adming -c "mkdir /home/adming/.ssh"

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDHTsWifYmpIvUb0Ge4ayFzzm1by0jiU30vgRZHMqRSLgkNel9NMbKoCwqgk+0KzaXoQr5LEL+ZAOzwWv+2bNtEF+NEquKW90COOXKmyKwRs7uKc+12YX3PCYbqU4ZOT7ApU0IHngY9jYme2y158yYCYmC9WrYOzJqMwsRMdoAt78NJt2rY08NXCgia34/jhO9CXw/nOY6yTF4i/GDYf1dlx7B9wzl7kYVb97wgEvTYZHLXEqAXhuqypEXaz5lJYFx+pxSjiBYOee2JJNE7ASleCGfGSoGcu4JwMKNJ3vABZPYB27W/F4GWh2D0DYog1m8mIJ4LRV49onwH47t/y+rX2kS9y/Ynv6Lb3FAW5BwGHzyNHxLYE1AAHa14tF/aQIF4rKpqgbEtW0iP+7UVus4Kn7eT5/xPw+/BlnBZc233yihvOLbcC94Adk7FwZ4Syav5dIeNUBSOJ9s/536Hh9IyU8Ieo1PdW8MAdwn+0mP4FdF7RUto8T1PZcveK2pTaNc= kabira@devel0.my.domain" > /tmp/x
su adming -c "cat /tmp/x >> ~/.ssh/authorized_keys"
