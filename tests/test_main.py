# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from unittest import mock

from wca import main

yaml_config = '''
runner: !DummyRunner
'''


@mock.patch('sys.argv', ['wca', '-c',
                         '/etc/configs/see_yaml_config_variable_above.yaml',
                         '-r', 'tests.testing:DummyRunner', '-l', 'critical',
                         '--root'])
@mock.patch('os.rmdir')
@mock.patch('wca.config.exists', return_value=True)
@mock.patch('wca.config.open', mock.mock_open(read_data=yaml_config))
@mock.patch('wca.perf.PerfCounters')
@mock.patch('wca.main.exit')
@mock.patch('wca.main.valid_config_file')
def test_main(*mocks):
    main.main()


yaml_config_unknown_field = '''
unknownRunner: !DummyRunner
runner: !DummyRunner
'''


@mock.patch('wca.main.log.error')
@mock.patch('sys.argv', ['wca', '-c',
                         '/etc/configs/see_yaml_config_variable_above.yaml',
                         '-r', 'tests.testing:DummyRunner', '-l', 'critical',
                         '--root'])
@mock.patch('os.rmdir')
@mock.patch('wca.config.exists', return_value=True)
@mock.patch('wca.config.open', mock.mock_open(
    read_data=yaml_config_unknown_field))
@mock.patch('wca.perf.PerfCounters')
@mock.patch('wca.main.exit')
@mock.patch('wca.main.valid_config_file')
def test_main_unknown_field(mock_valid_config_file, mock_exit, perf_counters, mock_rmdir,
                            mock_argv, mock_log_error):
    main.main()
    mock_log_error.assert_called_once_with('Error: Unknown field in '
                                           'configuration file: unknownRunner.'
                                           ' Possible fields are: \'loggers\', '
                                           '\'runner\'')


@mock.patch('wca.main.log.error')
@mock.patch('sys.argv', ['wca', '-c',
                         'configs/see_yaml_config_variable_above.yaml',
                         '-r', 'tests.testing:DummyRunner', '-l', 'critical',
                         '--root'])
@mock.patch('wca.config.exists', return_value=True)
@mock.patch('wca.config.open', mock.mock_open(read_data=yaml_config))
@mock.patch('wca.main.exit')
@mock.patch('os.stat')
@mock.patch('pwd.getpwuid')
def test_main_valid_config_file_not_absolute_path(mock_pwd, os_stat, mock_exit, mock_argv, mock_log_error):

    stat = mock.Mock()
    stat.st_size = 35
    stat.st_uid = 0
    stat.st_mode = 700
    os_stat.return_value = stat

    pwd = mock.Mock()
    pwd.pw_name = 'root'
    mock_pwd.return_value = pwd

    main.valid_config_file('configs/see_yaml_config_variable_above.yaml')
    mock_log_error.assert_called_once_with(
        'Error: The config path \'configs/see_yaml_config_variable_above.yaml\' is not valid. '
        'The path must be absolute.')


@mock.patch('wca.main.log.error')
@mock.patch('sys.argv', ['wca', '-c',
                         'configs/see_yaml_config_variable_above.yaml',
                         '-r', 'tests.testing:DummyRunner', '-l', 'critical',
                         '--root'])
@mock.patch('wca.config.exists', return_value=True)
@mock.patch('wca.config.open', mock.mock_open(read_data=yaml_config))
@mock.patch('wca.main.exit')
@mock.patch('os.stat')
@mock.patch('pwd.getpwuid')
def test_main_valid_config_file_wrong_user(mock_pwd, os_stat, mock_exit, mock_argv, mock_log_error):

    stat = mock.Mock()
    stat.st_size = 35
    stat.st_uid = 123123
    stat.st_mode = 700
    os_stat.return_value = stat

    pwd = mock.Mock()
    pwd.pw_name = 'root'
    mock_pwd.return_value = pwd

    main.valid_config_file('/etc/configs/see_yaml_config_variable_above.yaml')
    mock_log_error.assert_called_once_with(
        'Error: The config \'/etc/configs/see_yaml_config_variable_above.yaml\' is not valid. '
        'User is not owner config or is not root.')


@mock.patch('wca.main.log.error')
@mock.patch('sys.argv', ['wca', '-c',
                         'configs/see_yaml_config_variable_above.yaml',
                         '-r', 'tests.testing:DummyRunner', '-l', 'critical',
                         '--root'])
@mock.patch('wca.config.exists', return_value=True)
@mock.patch('wca.config.open', mock.mock_open(read_data=yaml_config))
@mock.patch('wca.main.exit')
@mock.patch('os.stat')
@mock.patch('pwd.getpwuid')
def test_main_valid_config_file_wrong_user(mock_pwd, os_stat, mock_exit, mock_argv, mock_log_error):

    stat = mock.Mock()
    stat.st_size = 35
    stat.st_uid = 0
    stat.st_mode = 777
    os_stat.return_value = stat

    pwd = mock.Mock()
    pwd.pw_name = 'root'
    mock_pwd.return_value = pwd

    main.valid_config_file('/etc/configs/see_yaml_config_variable_above.yaml')
    mock_log_error.assert_called_once_with(
        'Error: The config \'/etc/configs/see_yaml_config_variable_above.yaml\' is not valid. '
        'It has not correct proper ACLs. Only user have to have ability read and write.')
