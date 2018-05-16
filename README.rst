ansible-hostmanager
===================

CLI script to work with Ansible hosts file

To install::

    pip install ansible-hostmanager

To show hosts::

    $ ah list
    /etc/ansible/hosts exists and will be used. To change, run: ah set-hosts <PATH>
    Inventory has 4 host(s)
    app-server1         1.2.3.4   [app, all]
    web-server          1.2.3.5   [web, all]
    app-server2         1.2.3.6   [app, all]
    db-server           1.2.3.7   [db, all]

    $ ah list app
    app-server1         1.2.3.4   [app, all]
    app-server2         1.2.3.6   [app, all]

To ssh to a host::

    $ ah ssh db
    # Runs `ssh 1.2.3.7`

    $ ah ssh app
    Found multiple matches and will use first one: app-server1, app-server2
    # Runs `ssh 1.2.3.4`
