from localconfig import config
import pytest

from ansible_hostmanager import main


@pytest.fixture
def hosts_file(cli_runner, tmpdir):
    h_file = tmpdir.join('hosts')
    h_file.write('[app_server]\napp1 ansible_host=1.2.3.4\napp2')
    config.hosts_file = h_file
    return h_file


def test_set_hosts(cli_runner, hosts_file):
    result = cli_runner.invoke_and_assert_exit(0, main, ['set-hosts', str(hosts_file)])
    assert result.output == 'Inventory has 2 host(s)\n'


def test_hosts_file_not_set(cli_runner):
    config.hosts_file = None
    result = cli_runner.invoke_and_assert_exit(1, main, ['list'])
    assert result.output == 'Please set path to Ansible hosts file by running: ah set-hosts <PATH>\n'


def test_list_using_default_file(cli_runner, tmpdir):
    config.hosts_file = None
    hosts_file = tmpdir.join('hosts')
    hosts_file.write('[app]\napp1\napp2')

    import ansible_hostmanager
    ansible_hostmanager.DEFAULT_HOSTS_FILE = hosts_file
    result = cli_runner.invoke_and_assert_exit(0, main, ['list'])

    assert 'Inventory has 2 host(s)' in result.output


def test_list_with_unknown_host(cli_runner, tmpdir):
    result = cli_runner.invoke_and_assert_exit(1, main, ['list', 'blah'])
    assert result.output.startswith('No matching hosts found from inventory: ')


def test_list(cli_runner, hosts_file):
    result = cli_runner.invoke_and_assert_exit(0, main, ['list'])
    assert result.output == 'app1  1.2.3.4  [app_server, all]\napp2           [app_server, all]\n'


def test_list_name_only(cli_runner, hosts_file):
    result = cli_runner.invoke_and_assert_exit(0, main, ['list', '--name-only'])
    assert result.output == 'app1\napp2\n'


def test_ssh_exact_match(cli_runner, hosts_file, mock_run):
    result = cli_runner.invoke_and_assert_exit(0, main, ['ssh', 'app1'])
    mock_run.assert_called_with(['ssh', '1.2.3.4'])
    assert result.output == ''


def test_ssh_no_ip(cli_runner, hosts_file, mock_run):
    cli_runner.invoke_and_assert_exit(0, main, ['ssh', 'app2'])
    mock_run.assert_called_with(['ssh', 'app2'])


def test_ssh_multiple_matches(cli_runner, hosts_file, mock_run):
    result = cli_runner.invoke_and_assert_exit(0, main, ['ssh', 'app'])
    mock_run.assert_called_with(['ssh', '1.2.3.4'])
    assert result.output == 'Found multiple matches and will use first one: app1, app2\n'


def test_ssh_extra_args_after(cli_runner, hosts_file, mock_run):
    cli_runner.invoke_and_assert_exit(0, main, ['ssh', 'app', '-i', 'id'])
    mock_run.assert_called_with(['ssh', '1.2.3.4', '-i', 'id'])


def test_ssh_extra_args_before(cli_runner, hosts_file, mock_run):
    cli_runner.invoke_and_assert_exit(0, main, ['ssh', '-i', 'id', 'app'])
    mock_run.assert_called_with(['ssh', '-i', 'id', '1.2.3.4'])


def test_ssh_with_user(cli_runner, hosts_file, mock_run):
    cli_runner.invoke_and_assert_exit(0, main, ['ssh', '-i', 'id', 'max@app', '-T'])
    mock_run.assert_called_with(['ssh', '-i', 'id', 'max@1.2.3.4', '-T'])


def test_ssh_missing_args(cli_runner, hosts_file, mock_run):
    result = cli_runner.invoke_and_assert_exit(1, main, ['ssh'])
    assert result.output == 'Hostname is required\n'


def test_ssh_exception(cli_runner, hosts_file, mock_run):
    mock_run.side_effect = Exception('Kaboom!')
    result = cli_runner.invoke_and_assert_exit(1, main, ['ssh', 'app1'])
    mock_run.assert_called_with(['ssh', '1.2.3.4'])
    assert result.output == ''
