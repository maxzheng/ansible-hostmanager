ansible-hostmanager
===================

CLI script to work with Ansible hosts file

To install::

    pip install ansible-hostmanager

After installing, set location to Ansible `hosts` file::

    $ ah set-hosts ~/workspace/infra/cm/hosts
    Found 4 host(s)

To show hosts::

    $ ah list
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
