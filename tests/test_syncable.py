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
from configs.config_logger import setup_logging
from configs.commons import *
from sdk.ajxp_conf import *

setup_logging(logging.INFO)

def test_syncable(server_def, workspace):
    if 'syncable' in workspace['skip']:
        assert True
        return

    sdk = PydioSdk(server_def['host'], workspace['id'], unicode(''), '', (server_def['user'], server_def['pass']))
    sdk.stick_to_basic = True

    path = '/pydio-sync-file'
    changes = sdk.changes(0)
    last_seq = changes['last_seq']


    # CREATE FILE
    sdk.mkfile(path)
    # CHECK FILE IS IN CHANGES
    data = sdk.changes(last_seq)
    last_seq = data['last_seq']
    found = False
    for change in data['changes']:
        if change['source'] == 'NULL' and change['target'] == path and change['type'] == 'create':
            found = True
    assert found


    # DELETE FILE
    sdk.delete(path)
    # CHECK DELETION APPEARS IN CHANGES
    data = sdk.changes(last_seq)
    last_seq = data['last_seq']
    found = False
    for change in data['changes']:
        if change['source'] == path and change['target'] == 'NULL' and change['type'] == 'delete':
            found = True
    assert found

    # CREATE A MOVE
    sdk.mkfile(path)
    sdk.rename(path, path + '-moved')
    # CHECK DELETION APPEARS IN CHANGES
    data = sdk.changes(last_seq)
    last_seq = data['last_seq']
    found = False
    for change in data['changes']:
        if change['source'] == path and change['target'] == path + '-moved' and change['type'] == 'path':
            found = True
    sdk.delete(path + '-moved')
    assert found
