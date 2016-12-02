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
from sdk.ajxp_conf import *
import os, time,random, string
import pydioenv

setup_logging(logging.INFO)


def assert_file_exists(sdk, path, stat=None):
    result = sdk.list( os.path.dirname(path) )
    assert path in result
    if stat:
        assert int(result[path]) == stat['size']
    remote_stat = sdk.stat(path)
    if stat:
        assert int(remote_stat['size']) == stat['size']
    else:
        assert 'size' in remote_stat


def assert_file_deleted(sdk, path):
    result = sdk.list( os.path.dirname(path) )
    assert path not in result
    remote_stat = sdk.stat(path)
    assert not remote_stat


def random_folder_name(N):
    return unicode(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N)))


def create_delete(sdk, path):
    # CREATE FILE
    sdk.mkfile(path)
    # CHECK FILE IS IN LIST
    assert_file_exists(sdk, path)

    # DELETE FILE
    sdk.delete(path)
    # CHECK FILE IS NO MORE IN LIST
    assert_file_deleted(sdk, path)


def local_stat(path):
    stat_result = os.stat(path)
    s = dict()
    s['size'] = stat_result.st_size
    s['mtime'] = stat_result.st_mtime
    s['mode'] = stat_result.st_mode
    s['inode'] = stat_result.st_ino
    return s


def test_simple(server_def, workspace):
    if 'fs' in workspace['skip']:
        assert True
        return

    sdk = PydioSdk(server_def['host'], workspace['id'], unicode(''), '', (server_def['user'], server_def['pass']), skip_ssl_verify=pydioenv.noverify)
    sdk.stick_to_basic = True

    create_delete(sdk, '/pydio-simple-file')
    create_delete(sdk, '/fichié accentué'.decode('utf-8'))


def test_upload(server_def, workspace):
    sdk = PydioSdk(server_def['host'], workspace['id'], unicode(''), '', (server_def['user'], server_def['pass']), skip_ssl_verify=pydioenv.noverify)
    sdk.stick_to_basic = True

    stat = local_stat('resources/image.png')
    sdk.upload(local='resources/image.png', local_stat=local_stat('resources/image.png'), path=unicode('/image.png'))

    result = sdk.list('/')
    assert '/image.png' in result
    assert int(result['/image.png']) == stat['size']

    remote_stat = sdk.stat('/image.png')
    assert 'size' in remote_stat and remote_stat['size'] == stat['size']

    sdk.download(unicode('/image.png'), 'resources/downloaded_image.png')
    new_stat = local_stat('resources/downloaded_image.png')
    assert new_stat['size'] == stat['size']

    sdk.delete('/image.png')
    os.unlink('resources/downloaded_image.png')


def test_litmus(server_def, workspace):
    sdk = PydioSdk(server_def['host'], workspace['id'], unicode(''), '', (server_def['user'], server_def['pass']), skip_ssl_verify=pydioenv.noverify)
    sdk.stick_to_basic = True

    # Pure ASCII
    # Create random folder to make sure to start on a clean basis
    base = u'/' + random_folder_name(16)
    sdk.mkdir(base)
    assert_file_exists(sdk, base)

    filename = unicode(base + '/image.png')
    folder_name = unicode(base + '/folder')
    renamed_file = unicode(base + '/image-renamed.png')
    copied_file = unicode(base + '/folder/image-renamed.png')
    litmus_file(sdk, filename, renamed_file, folder_name, copied_file)

    sdk.delete(base)

    # UTF8 Characters
    base = u'/' + random_folder_name(16)
    sdk.mkdir(base)
    assert_file_exists(sdk, base)

    filename = unicode(base + u'/imagée.png')
    folder_name = unicode(base + u'/répertoire')
    renamed_file = unicode(base + u'/imagée-rennomée.png')
    copied_file = unicode(base + u'/répertoire/imagée-rennomée.png')
    litmus_file(sdk, filename, renamed_file, folder_name, copied_file)

    sdk.delete(base)


def litmus_file(sdk, filename, renamed_file, folder_name, copied_file):
    # Start by uploading a file
    local_image = 'resources/image.png'
    stat = local_stat(local_image)
    sdk.upload(local=local_image, local_stat=stat, path=filename)
    assert_file_exists(sdk, filename, stat)

    # Create a folder
    sdk.mkdir(folder_name)
    assert_file_exists(sdk, folder_name)

    # Rename image
    sdk.rename(filename, renamed_file)
    assert_file_exists(sdk, renamed_file, stat)
    assert_file_deleted(sdk, filename)

    # Copy image
    content = sdk.copy(renamed_file, folder_name)
    inner_debug(content)
    time.sleep(1)
    assert_file_exists(sdk, renamed_file, stat)
    assert_file_exists(sdk, copied_file, stat)

    # Remove folder recursively
    sdk.delete(folder_name)
    assert_file_deleted(sdk, folder_name)

    # Remove image
    sdk.delete(renamed_file)
    assert_file_deleted(sdk, renamed_file)
