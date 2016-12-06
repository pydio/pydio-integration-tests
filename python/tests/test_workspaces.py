#
#  Copyright 2007-2014 Charles du Jeu - Abstrium SAS <team (at) pyd.io>
#  This file is part of Pydio.
#
#  Pydio is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pydio is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Pydio.  If not, see <http://www.gnu.org/licenses/>.
#
#  The latest code can be found at <http://pyd.io/>.
#
from configs.config_logger import setup_logging
from configs.commons import *
from sdk.ajxp_conf import *
import pydioenv

setup_logging(logging.INFO)


def ls(server_def, repo_id, test_path='/recycle_bin'):
    sdk = PydioSdk(server_def['host'], repo_id, unicode(''), '', (server_def['user'], server_def['pass']), skip_ssl_verify=pydioenv.noverify)
    sdk.stick_to_basic = True
    result = sdk.list('/')
    inner_debug(result)
    if test_path in result:
        return True
    else:
        raise Exception("Cannot find /recycle_bin in listing")


def test_workspaces(server_def, workspace_def):
    repo = workspace_def['install_data']
    sdk = SettingsSdk(server_def)
    try:
        logging.info("[TESTING WORKSPACE %s]" % repo['DISPLAY'])
        new_id = sdk.create_repo(repo)
        if repo["DRIVER_OPTIONS"]["RECYCLE_BIN"]:
            testRes = ls(server_def, new_id)
            assert testRes
        logging.info("[> SUCCESS]")
        logging.info(" ")
    except Exception as e:
        logging.error(e)
        logging.error("[> ERROR]")
        assert False
    sdk.delete_repo(new_id)