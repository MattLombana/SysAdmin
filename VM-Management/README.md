
# Operating system setup and configuration

This directory contains a few ansible playbooks used to automate the setup of an operating system

## Table of Contents

* [How to use these playbooks](#how-to-use)


### How-To-use

Each one of these playbooks has settings that can be edited to tweak your needs. These variables and settings can be found in this directory as well as the [variables](./variables/) directory. You will need to edit 3 files in total. Templates have been provided. Once all three files have been properly modified, see [how to run](#how-to-run)

#### Files To Modify

* [hosts.local](./hosts.local.template)
* [ssh-config.local](./ssh-config.local.template)
* [all.local.yml](./variables/all.yml)

##### hosts.local

This file contains the info about each machine you plan on configuring. Each entry must map to one in ssh-config.local. There are several types of machines, each for each type of playbook. You may want to configure the ansible\_user and ansible\_become\_pass for each machine

##### ssh-config.local

This file contains the ssh connection information about each machine you plan on configuring. At a minimum, you must change the hostname and ip address of each machine.

##### all.local.yml

This file contains the configurable settings for the playbooks. Settings such as repos, programs and other sort of things will be defined in this file.

### How-To-Run

Once all the config files have been modified, you should run these playbooks from the ansible directory:

```bash
ansible-playbook -i hosts.local playbooks/example.yml
```
