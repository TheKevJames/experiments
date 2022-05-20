FROM debian:11

RUN apt-get -qy update && \
    apt-get -qy install --no-install-recommends \
        cloud-guest-utils \
        grub-pc-bin \
        grub2-common \
        isc-dhcp-client \
        linux-image-amd64 \
        openssh-server \
        sudo \
        systemd-sysv && \
    rm -rf /var/lib/apt/lists/*

COPY builtin/dhclient.service /etc/systemd/system/dhclient.service
COPY builtin/expand-root.service /etc/systemd/system/expand-root.service
COPY builtin/expand-root /usr/local/sbin/expand-root
RUN systemctl enable dhclient expand-root
