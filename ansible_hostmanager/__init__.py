import click
from pathlib import Path
import sys

from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from tabulate import tabulate
from utils.process import run

from localconfig import config


DEFAULT_HOSTS_FILE = Path('/etc/ansible/hosts')


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main():
    pass


@main.command('list')
@click.argument('partial_name', required=False)
@click.option('--name-only', is_flag=True, help='Show the hostname only')
def list_hosts(partial_name, name_only):
    """ List all hosts optionally filtered by partial name """
    hosts = []

    pattern = f'*{partial_name}*' if partial_name else 'all'
    for host in _hosts_matching(pattern):
        if name_only:
            hosts.append([host.name])
        else:
            hosts.append([host.name, host.vars.get('ansible_host'), host.groups])

    if hosts:
        click.echo(tabulate(sorted(hosts), tablefmt='plain'))
    else:
        click.echo('Host Inventory: ' + config.hosts_file)


@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('host')
@click.argument('ssh_args', nargs=-1, type=click.UNPROCESSED)
def ssh(host, ssh_args):
    """ Run ssh for the given host """
    hosts = _hosts_matching(host)
    if hosts:
        if len(hosts) > 1:
            click.echo('Found multiple matches and will use first one: ' + ', '.join(h.name for h in hosts))

        try:
            run(['ssh', hosts[0].vars.get('ansible_host', hosts[0].name)] + list(ssh_args))

        except Exception as e:
            pass


@main.command('set-hosts')
@click.argument('hosts_file')
def set_hosts(hosts_file):
    """ Set hosts file """
    _set_hosts(hosts_file)


def _set_hosts(hosts_file):
    config.hosts_file = hosts_file
    config.save()

    inventory = _get_inventory()

    click.echo('Inventory has {} host(s)'.format(len(inventory.hosts)))


def _hosts_matching(hostname):
    """ Returns a list of hosts matching the hostname exactly or partially """
    inventory = _get_inventory()

    if hostname in inventory.hosts:
        return [inventory.hosts[hostname]]
    else:
        return inventory.list_hosts(f'*{hostname}*')


def _get_inventory():
    if not config.hosts_file:
        if DEFAULT_HOSTS_FILE.exists():
            click.echo('{} exists and will be used. To change, '
                       'run: ah set-hosts <PATH>'.format(DEFAULT_HOSTS_FILE))
            _set_hosts(str(DEFAULT_HOSTS_FILE))

        else:
            click.echo('Please set path to Ansible hosts file by running: ah set-hosts <PATH>')
            sys.exit(1)

    return InventoryManager(loader=DataLoader(), sources=config.hosts_file)
