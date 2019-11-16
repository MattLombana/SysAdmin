
# Operating system setup and configuration

This directory contains a few ansible playbooks used to automate the setup of an operating system

## Table of Contents

* [How to use these playbooks](#how-to-use)


### How-To-use

Each one of these playbooks has settings that can be edited to tweak your needs. These variables and
settings can be found in this directory as well as the [group_vars](./group_vars/) directory. You
will need to edit several files. Templates have been provided. Once all files have been
properly modified, see [how to run](#how-to-run)

#### Files To Modify

* [hosts.local](./hosts.local.template)
* [ssh-config.local](./ssh-config.local.template)
* [all.local.yml](./group_vars/all.yml)
* [vault.local.yml](./group_vars/vault.yml)
* [Various other variable files](./group_vars/)

##### hosts.local

This file contains the info about each machine you plan on configuring. Each entry must map to one
in ssh-config.local. There are several types of machines, each for each type of playbook. You may
want to configure the ansible\_user and ansible\_become\_pass for each machine
```
cp ./hosts.local.template ./hosts.local
vim ./hosts.local
```

##### ssh-config.local

This file contains the ssh connection information about each machine you plan on configuring. At a
minimum, you must change the hostname and ip address of each machine.
```
cp ./ssh-config.local.template ./ssh-config.local
vim ./ssh-config.local
```

##### all.local.yml

This file contains the configurable settings for the playbooks. Settings such as repos, programs and
other sort of things will be defined in this file.

```
cp ./group_vars/all.yml ./group_vars/all.local.yml
vim ./group_vars/all.yml
```

##### vault.local.yml

This is the ansible vault that contains sensitive data. This includes the ansible_become_pass, user
passwords, passwords to mount files, and many other items. Read more about vaults
[here](https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html)

```
cp ./group_vars/vault.yml ./group_vars/vault.local.yml
ansible-vault encrypt ./group_vars/vault.local.yml
ansible-vault edit ./group_vars/vault.local.yml
```

### How-To-Run

Once all the config files have been modified, you should run these playbooks from the ansible
directory:

```
ansible-playbook playbooks/example.yml
```

Note, if you do not want to enter the vault password, you can create a
.vault_pass file and uncomment the following line to ansible.cfg under `[defaults]`:

```
vault_password_file = ./.vault_pass
```
