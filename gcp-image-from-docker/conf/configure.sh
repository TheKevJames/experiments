#!/usr/bin/env bash
set -euo pipefail

trap '{ umount /os/mnt/dev; umount /os/mnt; dmsetup remove_all; losetup -D; rm -f /dev/loop0p1; }' EXIT

apt-get update -qy
apt-get install -qy multipath-tools

rm -f /os/disk.img
dd if=/dev/zero of=/os/disk.img bs=$((2 * 1024 ** 3)) count=1
sfdisk /os/disk.img < /os/conf/sfdisk.part

losetup -P /dev/loop0 /os/disk.img
kpartx -va /dev/loop0
mknod /dev/loop0p1 b 259 0
losetup /dev/loop1 /dev/loop0p1

mkfs.ext3 /dev/loop1

mkdir -p /os/mnt
mount -t auto /dev/loop1 /os/mnt/
tar xf /os/disk.tar -C /os/mnt/

mkdir -p /os/mnt/boot/grub
cp /os/conf/device.map /os/mnt/boot/grub/device.map
mount --bind /dev /os/mnt/dev

cp /os/mnt/usr/share/grub/default/grub /os/mnt/etc/default/grub
sed -i 's/quiet/console=ttyS0,38400n8d/' /os/mnt/etc/default/grub
sed -i 's/GRUB_TIMEOUT=5/GRUB_TIMEOUT=0/' /os/mnt/etc/default/grub

chroot /os/mnt grub-mkconfig -o /boot/grub/grub.cfg
sed -i 's/loop0p1/sda1/' /os/mnt/boot/grub/grub.cfg

grub-install --no-floppy \
    --boot-directory=/os/mnt/boot \
    --modules="ext2 part_msdos" \
    /dev/loop0
chroot /os/mnt grub-mkdevicemap

blkid | awk '/loop1/ {print "UUID="substr($2, 7, length($2)-7)"\011/\011ext3\011defaults\0111\0111"}' > /os/mnt/etc/fstab

mkdir -p /os/mnt/etc/systemd/system/getty@.service.d
cp /os/builtin/getty.service.override /os/mnt/etc/systemd/system/getty@.service.d/override.conf
echo '127.0.0.1 localhost' > /os/mnt/etc/hosts
echo 'ALL     ALL = (ALL) NOPASSWD: ALL' >> /os/mnt/etc/sudoers
echo 'server metadata.google.internal iburst' > /os/mnt/etc/ntp.conf
echo 'net.ipv6.conf.all.disable_ipv6 = 1' > /os/mnt/etc/sysctl.conf

sed -i 's/^#\?PermitRootLogin .*$/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^#\?PasswordAuthentication .*$/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#\?HostbasedAuthentication .*$/HostbasedAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#\?AllowTcpForwarding .*$/AllowTcpForwarding yes/' /etc/ssh/sshd_config
sed -i 's/^#\?PermitTunnel .*$/PermitTunnel no/' /etc/ssh/sshd_config
sed -i 's/^#\?X11Forwarding .*$/X11Forwarding no/' /etc/ssh/sshd_config
sed -i 's/^#\?ClientAliveInterval .*$/ClientAliveInterval 420/' /etc/ssh/sshd_config
cp /os/builtin/ssh_config /os/mnt/etc/ssh/ssh_config
