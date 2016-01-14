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
from configs.commons import *
from sdk.ajxp_conf import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


def detect_shared_link(url, expect_working=True):
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(5)

    assert "Pydio" in driver.title

    try:
        if expect_working:
            element = driver.find_element_by_id('mainImage')
        else:
            element = driver.find_element_by_css_selector('div.hash_load_error')
    except NoSuchElementException:
        assert False

    assert element

    driver.close()


def local_stat(path):
    import os
    stat_result = os.stat(path)
    s = dict()
    s['size'] = stat_result.st_size
    s['mtime'] = stat_result.st_mtime
    s['mode'] = stat_result.st_mode
    s['inode'] = stat_result.st_ino
    return s


def test_shared_link(server_def, workspace):
    sdk = PydioSdk(server_def['host'], workspace['id'], unicode(''), '', (server_def['user'], server_def['pass']))

    sdk.upload(local='resources/image.png', local_stat=local_stat('resources/image.png'), path=unicode('/image.png'))
    link = sdk.share('Shared File', 'Description', '', '', '', 'true', 'true', u'/image.png', '', 'false')
    detect_shared_link(link, expect_working=True)
    sdk.unshare(u'/image.png')
    detect_shared_link(link, expect_working=False)
    sdk.delete('/image.png')