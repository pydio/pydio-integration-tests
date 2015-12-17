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
from sdk.remote import PydioSdk
import logging
import xml.etree.ElementTree as ET
from configs.config_logger import setup_logging
from configs.fixtures import *

setup_logging(logging.INFO)

def inner_debug(message):
    logging.info("  | %s" % message)


def ls(server_def, repo_id, test_path='/recycle_bin'):
    sdk = PydioSdk(server_def['host'], repo_id, unicode(''), '', (server_def['user'], server_def['pass']))
    sdk.stick_to_basic = True
    result = sdk.list('/')
    inner_debug(result)
    if test_path in result:
        return True
    else:
        raise Exception("Cannot find /recycle_bin in listing")


def write(server_def, repo_id):
    sdk = PydioSdk(server_def['host'], repo_id, unicode(''), '', (server_def['user'], server_def['pass']))
    sdk.stick_to_basic = True
    sdk.mkfile('/pydio-testing-test_file')


def create_repo(server_def, repo_def):
    sdk = PydioSdk(server_def['host'], 'ajxp_conf', unicode(''), '', (server_def['user'], server_def['pass']))
    sdk.stick_to_basic = True
    import json
    json_data = json.dumps(repo_def)
    resp = sdk.perform_request(sdk.url+'/create_repository/'+json_data, 'post')
    inner_debug(resp.content)
    queue = [ET.ElementTree(ET.fromstring(resp.content)).getroot()]
    tree = queue.pop(0)
    message = tree.findall('message').pop(0)
    if message.get('type') == 'SUCCESS':
        reload_node = tree.findall('reload_instruction').pop(0)
        new_repo_id = reload_node.get('file')
        return new_repo_id
    else:
        raise Exception('Error while creating workspace')


def delete_repo(server_def, repo_id):
    sdk = PydioSdk(server_def['host'], 'ajxp_conf', unicode(''), '', (server_def['user'], server_def['pass']))
    sdk.stick_to_basic = True
    resp = sdk.perform_request(sdk.url+'/delete/repository/'+repo_id)
    inner_debug(resp.content)


def test_workspaces(server_def, workspaces_defs):
    for repo in workspaces_defs:
        try:
            logging.info("[TESTING WORKSPACE %s]" % repo['DISPLAY'])
            new_id = create_repo(server_def, repo)
            testRes = ls(server_def, new_id)
            delete_repo(server_def, new_id)
            logging.info("[> SUCCESS]")
            logging.info(" ")
            assert testRes
        except Exception as e:
            logging.error(e)
            logging.error("[> ERROR]")
            assert False
