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
from sdk.remote import PydioSdk
import logging
from configs.config_logger import setup_logging
from configs.commons import *
from sdk.ajxp_conf import *

setup_logging(logging.INFO)

def test_fs(server_def, workspaces_defs):

    repo_id = create_repo(server_def, workspaces_defs[0])
    sdk = PydioSdk(server_def['host'], repo_id, unicode(''), '', (server_def['user'], server_def['pass']))
    sdk.stick_to_basic = True

    path = '/pydio-simple-file'

    # CREATE FILE
    sdk.mkfile(path)
    # CHECK FILE IS IN LIST
    result = sdk.list('/')
    inner_debug(result)
    assert path in result

    # DELETE FILE
    sdk.delete(path)
    # CHECK FILE IS NO MORE IN LIST
    result = sdk.list('/')
    inner_debug(result)
    assert path not in result

    delete_repo(server_def, repo_id)