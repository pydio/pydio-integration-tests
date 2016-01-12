#
# Copyright 2007-2014 Charles du Jeu - Abstrium SAS <team (at) pyd.io>
#  This file is part of Pydio.
#
#  Pydio is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pydio is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Pydio.  If not, see <http://www.gnu.org/licenses/>.
#
#  The latest code can be found at <http://pyd.io/>.
#
import pytest, json, logging, os


def inner_debug(message):
    logging.info("  | %s" % message)


def pytest_generate_tests(metafunc):
    if 'server_config_file' in metafunc.fixturenames:
        i = 0
        files = []
        while os.path.exists('configs/server.' + str(i) + '.json'):
            files.append('configs/server.' + str(i) + '.json')
            i += 1
        metafunc.parametrize("server_config_file", files)

    if 'workspace_config_file' in metafunc.fixturenames:
        i = 0
        files = []
        while os.path.exists('configs/workspace.' + str(i) + '.json'):
            with open('configs/workspace.' + str(i) + '.json') as handler:
                j_dict = json.load(handler)
                if metafunc.module.__name__ in j_dict['skip']:
                    i += 1
                    continue
            files.append('configs/workspace.' + str(i) + '.json')
            i += 1
        metafunc.parametrize("workspace_config_file", files)


@pytest.fixture
def server_def(server_config_file):
    with open(server_config_file) as handler:
        jDict = json.load(handler)
    return jDict


@pytest.fixture
def workspace_def(workspace_config_file):
    with open(workspace_config_file) as handler:
        jDict = json.load(handler)
    return jDict


@pytest.fixture
def workspace(request, server_def, workspace_def):
    from sdk.ajxp_conf import create_repo, delete_repo
    repo_id = create_repo(server_def, workspace_def['install_data'])
    workspace_def['id'] = repo_id
    def fin():
        print ("teardown repo")
        delete_repo(server_def, repo_id)
    request.addfinalizer(fin)
    return workspace_def