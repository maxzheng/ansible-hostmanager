from localconfig import config

from ansible_hostmanager import main


def test_hostmanager(cli_runner, tmpdir, mock_run):
    config.hosts_file = None
    result = cli_runner.invoke_and_assert_exit(1, main, ['list'])
    assert result.output == 'Please set path to Ansible hosts file by running: ah set-hosts <PATH>\n'

    # Uses default file
    config.hosts_file = None
    hosts_file = tmpdir.join('hosts')
    hosts_file.write('[app]\napp1\napp2')
    import ansible_hostmanager
    ansible_hostmanager.DEFAULT_HOSTS_FILE = hosts_file
    result = cli_runner.invoke_and_assert_exit(0, main, ['list', str(hosts_file)])
    assert 'Inventory has 2 host(s)' in result.output
    ansible_hostmanager.DEFAULT_HOSTS_FILE = '/etc/blah'

    # Set hosts
    config.hosts_file = None
    hosts_file = tmpdir.join('hosts')
    result = cli_runner.invoke_and_assert_exit(0, main, ['set-hosts', str(hosts_file)])

    # List
    hosts_file.write('[app_server]\napp1 ansible_host=1.2.3.4\napp2')
    result = cli_runner.invoke_and_assert_exit(0, main, ['list'])
    assert result.output == 'app1  1.2.3.4  [app_server, all]\napp2           [app_server, all]\n'

    # SSH -- Exact match
    result = cli_runner.invoke_and_assert_exit(0, main, ['ssh', 'app1'])
    mock_run.assert_called_with(['ssh', '1.2.3.4'])
    assert result.output == ''

    # SSH - No IP
    result = cli_runner.invoke_and_assert_exit(0, main, ['ssh', 'app2'])
    mock_run.assert_called_with(['ssh', 'app2'])

    # SSH - Multiple matches
    result = cli_runner.invoke_and_assert_exit(0, main, ['ssh', 'app'])
    mock_run.assert_called_with(['ssh', '1.2.3.4'])
    assert result.output == 'Found multiple matches and will use first one: app1, app2\n'
