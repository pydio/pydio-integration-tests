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
import pydioenv

setup_logging(logging.INFO)


def test_zip(server_def, workspace):
    sdk = PydioSdk(server_def['host'], workspace['id'], unicode(''), '', (server_def['user'], server_def['pass']), skip_ssl_verify=pydioenv.noverify)
    sdk.stick_to_basic = True

    path = '/pydio-simple-file'

    # CREATE FOLDERS
    sdk.bulk_mkdir(['/a', '/a/b', '/a/b/c', '/a/b/d'])
    result = sdk.list(unicode('/a/b'))
    assert '/a/b/c' in result
    assert '/a/b/d' in result

    # CREATE ZIP FROM FOLDER A
    data = dict()
    data['archive_name'] = 'a.zip'
    sdk.perform_request(sdk.url + '/compress/a', data=data, type='post')
    result = sdk.list('')
    assert '/a.zip' in result

    result = sdk.list(unicode('/a.zip'))
    assert '/a.zip/a' in result

    result = sdk.list(unicode('/a.zip/a/b'))
    assert '/a.zip/a/b/c' in result
    assert '/a.zip/a/b/d' in result

    sdk.delete('/a')
    sdk.delete('/a.zip')
