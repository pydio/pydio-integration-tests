# coding=utf-8
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
from sdk.meta_sdk import *
import pydioenv

setup_logging(logging.INFO)


def test_meta_user(server_def, workspace):

    if 'META_SOURCES' not in workspace['install_data']['DRIVER_OPTIONS'] or 'meta.user' not in workspace['install_data']['DRIVER_OPTIONS']['META_SOURCES']:
        return
    meta_user_data = workspace['install_data']['DRIVER_OPTIONS']['META_SOURCES']['meta.user']
    meta_field = meta_user_data['meta_fields']
    meta_data_dict = dict()
    meta_data_dict[meta_field] = 'metadata_test_value'

    # Test update meta and read
    file_path = unicode('/empty_file')
    sdk = MetaSdk(server_def['host'], workspace['id'], unicode(''), '', (server_def['user'], server_def['pass']), skip_ssl_verify=pydioenv.noverify)
    sdk.stick_to_basic = True

    sdk.mkfile(file_path)
    resp = sdk.edit_user_meta(file_path, meta_data_dict)

#    returned_meta = False

    def callback(tree_node):
        global returned_meta
        if tree_node['filename'] == file_path and meta_field in tree_node and tree_node[meta_field] == 'metadata_test_value':
            returned_meta = True

    sdk.list('/', call_back=callback)

    assert returned_meta