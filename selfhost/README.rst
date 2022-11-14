Selfhosted Platform
===================

Building up the things I selfhost as a source-controlled project. Goal here is
to have a single source for configuring all the things -- or at least a single
place where it's all documented, when that's not possible.

Setup
-----

`Install Raspbian OS Lite x64`_. Make sure to hit the options and pre-configure
wifi/hostname/ssh creds/etc before writing the image. Then ssh into the box
and set things up: you'll probably want to check out `Mounting External
Drives`_ first, then you can do the following:

.. code-block:: console

    ## PI
    # use the visual setup to configure yourself the correct locale
    $ sudo raspi-config

    ## PI-HOLE
    # follow the visual prompts
    $ curl -sSL https://install.pi-hole.net | bash
    # set your admin panel password, if you enabled it
    $ sudo pihole -a -p

    # verify it's working at the web portal and with:
    $ pihole status
    # verify from one of your client machines that the DNS resolver is working
    $ dig -4 @PI_IP_ADDRESS example.com

    # if not, a `sudo poweroff --reboot` after the first install can help
    # if you have issues with the above, here's some things which have helped:
    # reboot: `sudo poweroff --reboot`
    # update: `pihole -up`
    # update blocklists: `pihole -g` (sometimes these seem to be initialized
    # badly at first?)

    # now is also a great time to set up IPv6:
    # /admin/settings.php?tab=dns to toggle it on
    # get the ip with `ip -6 addr show | grep global`
    $ dig -6 @PI_IPV6_ADDRESS example.com

    # update your router/clients to start using the pihole
    # https://docs.pi-hole.net/main/post-install/
    # note that if you want fallback DNS addresses, I like Cloudflare:
    #   1.1.1.1, 1.0.0.1
    #   2606:4700:4700::1111, 2606:4700:4700::1001
    # verify that worked with
    $ dig -4 example.com | grep SERVER
    $ dig -6 example.com | grep SERVER
    # the SERVER should be using the IPv4 and IPv6 addresses you found earlier

    # upgrade and restart
    $ sudo apt upgrade -y
    $ sudo poweroff --reboot

    ## DOCKER
    # install docker
    # TODO: switch over to podman once raspbian supports it without manual
    # compilation and dealing with boostrapping multiple go versions
    $ curl -fsSL https://get.docker.com -o get-docker.sh
    $ sudo sh ./get-docker.sh

    ## HASS, Dashy
    # install dependencies we'll need later
    $ sudo apt update -y
    $ sudo apt install -y git

    # grab the config
    $ git clone https://github.com/TheKevJames/experiments ~/src/experiments
    $ cd ~/src/experiments/selfhost

    # configure any secrets in your config
    $ vi ./hass/secrets.yaml
    # restore any backups (gitignore'd by default!)
    # scp FOO pi@pihole:~/src/experiments/selfhost/hass/

    # start hass
    $ sudo docker compose pull
    $ sudo docker compose up -d

    # setup the admin account, unless you restored from a backup
    # visit http://pi.hole:8123/

Updates
-------

To update the various components:

.. code-block:: console

    sudo apt update -y
    sudo apt upgrade -y

    pihole -up

    cd ~/src/experiments/selfhost
    git pull

    sudo docker compose pull
    sudo docker compose down
    sudo docker compose up -d

Mounting External Disks
-----------------------

Quick walkthrough of how to fstab some external drives into being auto-mounted:

.. code-block:: console

    $ lsblk -f
    NAME        FSTYPE FSVER LABEL  UUID                                 FSAVAIL FSUSE% MOUNTPOINT
    sda
    `-sda1      ext4   1.0          43162a5a-f1b2-441f-9d51-433bea2e113c
    sdb
    `-sdb1      ext4   1.0          b9479cb5-b306-430b-998d-3d793aadfde6
    mmcblk0
    |-mmcblk0p1 vfat   FAT32 boot   0F92-BECC
    `-mmcblk0p2 ext4   1.0   rootfs 41c98998-6a08-4389-bf74-79c9efcf0739   26.4G     5% /

    # manually mount them
    $ sudo mkdir /mnt/1tb /mnt/4tb
    $ sudo mount /dev/sda1 /mnt/4tb
    $ sudo mount /dev/sdb1 /mnt/1tb

    # grab their details
    $ sudo blkid
    /dev/mmcblk0p1: LABEL_FATBOOT="boot" LABEL="boot" UUID="0F92-BECC" BLOCK_SIZE="512" TYPE="vfat" PARTUUID="620d2702-01"
    /dev/mmcblk0p2: LABEL="rootfs" UUID="41c98998-6a08-4389-bf74-79c9efcf0739" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="620d2702-02"
    /dev/sda1: UUID="43162a5a-f1b2-441f-9d51-433bea2e113c" BLOCK_SIZE="4096" TYPE="ext4" PARTLABEL="logical" PARTUUID="2570b09b-b7ea-407d-b1b7-9738fee48c80"
    /dev/sdb1: UUID="b9479cb5-b306-430b-998d-3d793aadfde6" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="555b5ad7-01"

    # auto-mount 'em at startup
    $ echo "UUID=43162a5a-f1b2-441f-9d51-433bea2e113c /mnt/4tb  ext4  defaults,noatime  0 0" | sudo tee -a /etc/fstab
    $ echo "UUID=b9479cb5-b306-430b-998d-3d793aadfde6 /mnt/1tb  ext4  defaults,noatime  0 0" | sudo tee -a /etc/fstab

    # mount 'em now
    $ sudo mount -a

TODOs
-----

* transmission
* hass > gcp?
* hass > gcal
* hass > spotify
* investigate multi-pi
* look at some of the new things from r/selfhost that I have bookmarked...
* need to actually fixup the ``home.thekev.in`` mapping. Does HASS' cloudflare
  integration solve those issues? How can I make that work with the multiple
  Pi's handling different svcs on different ports?

.. _Install Raspbian OS Lite x64: https://www.raspberrypi.com/software/
