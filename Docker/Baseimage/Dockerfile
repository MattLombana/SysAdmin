# FROM scratch
# FROM alpine:3.7
FROM phusion/baseimage

MAINTAINER Matt Lombana mlombana@mattlombana.com

WORKDIR /

# Install
RUN apt-get update && \
 apt-get install --no-install-recommends -y \
  build-essential \
  curl \
  git \
  unzip \
  vim \
  wget \
  ruby \
  ruby-dev \
  clamav-daemon \
  openssh-client \
  man \
  net-tools \
  iproute2 \
  netcat \
  nmap \
  && \
 rm -rf /var/lib/apt/lists/*

# Set ClamAV
RUN freshclam -v && \
 mkdir /var/run/clamav && \
 chown clamav:clamav /var/run/clamav && \
 chmod 750 /var/run/clamav
COPY ../../Configs/ClamAV/clamd.conf /etc/clamav/clamd.conf
COPY ../../Slack-Notifications/virus_message_slack.sh /etc/clamav/virus_message_slack.sh
RUN chown clamav:clamav /etc/clamav/virus_message_slack.sh && \
 chmod 750 /etc/clamav/virus_message_slack.sh


# TODO: Set NTP

# TODO: Set up SSH
 # Harden SSH
 # Add ssh-notification script
 # Add my host key to SSH
 # Long-term: use certs

# TODO: Decide: Add container as computer in AD if its long-living?

# Setup fail2ban

# TODO: Set firewall

# Define environment variables
ENV HOME "/root"

# Define working directory
WORKDIR /root

# Set PS1
RUN echo 'PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[38;5;160m\]\u@\[\033[38;5;208m\]\h:\w\$\[\033[00m\] "' >> ~/.bashrc

# Define default command
CMD ["/bin/bash"]
