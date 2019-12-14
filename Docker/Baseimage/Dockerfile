# FROM scratch
# FROM alpine:3.7
FROM phusion/baseimage
MAINTAINER Matt Lombana mlombana@mattlombana.com
WORKDIR /

####################################################################################################
#                         To add a new daemon, follow the instructions at                          #
#              https://github.com/phusion/baseimage-docker\#adding-additional-daemons              #
#                                                                                                  #
#               To run a script during container startup, follow the instructions at               #
#      https://github.com/phusion/baseimage-docker\#running-scripts-during-container-startup       #
####################################################################################################

################################################################################
#                                                                              #
#   Defaults to change before building:                                        #
#     - This adds a default insecure ssh key                                   #
#     - This adds the 'docker' user with the password 'Password1234'           #
#     - The slack notification URLs need to be changed                         #
#                                                                              #
################################################################################

################################################################################
#                             Install Basic Tools                              #
################################################################################
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
                    ufw

################################################################################
#                                 ClamAV Setup                                 #
################################################################################
########################################
#         Configure ClamAV and         #
#       Update Virus Definitions       #
########################################
RUN freshclam -v && \
    mkdir /var/run/clamav && \
    chown clamav:clamav /var/run/clamav && \
    chmod 750 /var/run/clamav
COPY ./Configs/ClamAV/clamd.conf /etc/clamav/clamd.conf

########################################
#      ClamAV Slack Notifications      #
########################################
COPY ./Slack-Notifications/virus_message_slack.sh /etc/clamav/virus_message_slack.sh
RUN chown clamav:clamav /etc/clamav/virus_message_slack.sh && \
    chmod 750 /etc/clamav/virus_message_slack.sh

########################################
#            Enable ClamAV             #
########################################
RUN mkdir /etc/service/clamav
COPY ./Configs/ClamAV/clamav.sh /etc/service/clamav/run
RUN chmod +x /etc/service/clamav/run


################################################################################
#                                  NTP Setup                                   #
################################################################################
# TODO: Setup NTP


################################################################################
#                                  SSH Setup                                   #
################################################################################
# TODO (Long-term): use ssh certs and lock down the default configuration

########################################
#         Copy Configurations          #
########################################
COPY ./Configs/SSH/sshd_config /etc/ssh/sshd_config
COPY ./Configs/SSH/banner /etc/ssh/banner

########################################
#       SSH Slack Notifications        #
########################################
COPY ./Slack-Notifications/ssh_message_slack.sh /etc/ssh/ssh_message_slack.sh
RUN chmod +x /etc/ssh/ssh_message_slack.sh && \
    echo 'session   optional      pam_exec.so /etc/ssh/ssh_message_slack.sh' >> /etc/pam.d/sshd

########################################
#          Expose and Enable           #
########################################
EXPOSE 22/tcp
RUN rm -f /etc/service/sshd/down && \
    /etc/my_init.d/00_regen_ssh_host_keys.sh


################################################################################
#                                User Creation                                 #
################################################################################
########################################
#        Create A Default User         #
#          and Set Their PS1           #
########################################
RUN useradd -ms /bin/bash -p $(openssl passwd -1 Password1234) docker && \
    echo 'PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[38;5;160m\]\u@\[\033[38;5;208m\]\h:\w\$\[\033[00m\] "' >> /home/docker/.bashrc

########################################
#       Add An Insecure SSH Key        #
########################################
RUN mkdir /home/docker/.ssh && \
    chown docker:docker /home/docker/.ssh && \
    chmod 0700 /home/docker/.ssh
COPY ./Configs/SSH/ssh_keys/insecure_key.pub /home/docker/.ssh/authorized_keys


################################################################################
#                                Fail2Ban Setup                                #
################################################################################
################################################################################
#                                Firewall Setup                                #
################################################################################
################################################################################
#                            Active Directory Setup                            #
################################################################################



################################################################################
#                               General Settings                               #
################################################################################
########################################
#        Environment Variables         #
########################################
ENV HOME "/root"

########################################
#          Working Directory           #
########################################
WORKDIR /root

########################################
#                 PS1                  #
########################################
RUN echo 'PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[38;5;160m\]\u@\[\033[38;5;208m\]\h:\w\$\[\033[00m\] "' >> ~/.bashrc

########################################
#        Clean Up APT When Done        #
########################################
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

########################################
#           Default Command            #
########################################
ENTRYPOINT ["/sbin/my_init"]
CMD ["/bin/sleep", "3600"]
