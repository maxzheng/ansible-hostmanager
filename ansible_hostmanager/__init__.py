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


@main.command()
@click.argument('partial_name', required=False)
def list(partial_name):
    """ List all hosts where name contains optional partial name """
    inventory = _get_inventory()

    hosts = []
    pattern = f'*{partial_name}*' if partial_name else 'all'
    for host in inventory.list_hosts(pattern):
        hosts.append([host.name, host.vars.get('ansible_host'), host.groups])

    if hosts:
        click.echo(tabulate(sorted(hosts), tablefmt='plain'))
    else:
        click.echo('Host Inventory: ' + config.hosts_file)


@main.command()
@click.argument('host')
def ssh(host):
    """ Run ssh for the given host """
    inventory = _get_inventory()

    hosts = inventory.list_hosts(f'*{host}*')

    if hosts:
        if len(hosts) > 1:
            click.echo('Found multiple matches and will use first one: ' + ', '.join(h.name for h in hosts))

        try:
            run(['ssh', hosts[0].vars.get('ansible_host', hosts[0].name)])

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
