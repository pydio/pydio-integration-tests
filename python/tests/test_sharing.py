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
from configs.commons import *
from sdk.ajxp_conf import *
from selenium.common.exceptions import NoSuchElementException
import time


def element_present(webdriver, id='', css='', test_attribute=''):
    try:
        if id:
            element = webdriver.find_element_by_id(id)
        else:
            element = webdriver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False

    if element and test_attribute:
        if not element.get_attribute(test_attribute):
            return False

    return True


def detect_shared_link(webdriver, url, expect_working=True, preview=True, download=True, trigger_download=0):
    time.sleep(1)
    webdriver.get(url)
    time.sleep(5)

    assert "Pydio" in webdriver.title

    if expect_working:
        test_att = 'style' if preview else ''
        preview_block_test = element_present(webdriver, css='.diaporama-image-main-block', test_attribute=test_att)
        result = (preview and preview_block_test) or (not preview and not preview_block_test)
        assert result

        if preview:
            download_block_test = element_present(webdriver, css='.action-download')
            if trigger_download > 0:
                for i in range(0, trigger_download):
                    webdriver.find_element_by_css_selector('.action-download').click()
                    time.sleep(2)
                    i += 1
        else:
            download_block_test = element_present(webdriver, css='.download-block')
        result = (download and download_block_test) or (not download and not download_block_test)
        assert result
    else:
        error_block_test = element_present(webdriver, css='div.hash_load_error')
        assert error_block_test


def detect_password_share_and_submit(web_driver, url, password):
    web_driver.get(url)
    time.sleep(5)

    assert "Pydio" in web_driver.title

    try:
        pass_field = web_driver.find_element_by_id('application-password')
        pass_field.send_keys(password)
        time.sleep(1)
        submit = web_driver.find_element_by_id('dialog-login-submit')
        submit.click()
        time.sleep(5)
        # Now check shared link
        assert element_present(web_driver, css='.diaporama-image-main-block', test_attribute='style')
        return True

    except NoSuchElementException:
        return False


def check_shared_element_data(sdk, filepath):
    s_data = sdk.check_share_link(filepath)
    data = json.loads(s_data)
    if 'links' in data:
        for key in data['links']:
            return data['links'][key]['public_link']
    return False


def local_stat(path):
    import os
    stat_result = os.stat(path)
    s = dict()
    s['size'] = stat_result.st_size
    s['mtime'] = stat_result.st_mtime
    s['mode'] = stat_result.st_mode
    s['inode'] = stat_result.st_ino
    return s

@pytest.mark.parametrize("preview,download", [
    (True, True),
    (True, False),
    (False, True),
])
def test_shared_link(server_def, workspace, webdriver, preview, download):
    sdk = PydioSdk(server_def['host'], workspace['id'], unicode(''), '', (server_def['user'], server_def['pass']))

    dl_right = 'true' if download else 'false'
    read_right = 'true' if preview else 'false'
    print 'read =' + read_right
    print 'dl =' + dl_right
    sdk.upload(local='resources/image.png', local_stat=local_stat('resources/image.png'), path=unicode('/image.png'))
    link = sdk.share(ws_label='Shared File', ws_description='Description', password='', expiration='', downloads='',
                     can_read=read_right, can_download=dl_right, paths=u'/image.png', link_handler='', can_write='false')
    detect_shared_link(webdriver, link, expect_working=True, preview=preview, download=download)

    # Unshare. At first pass, detect correctly unshared.
    sdk.unshare(u'/image.png')
    if preview and download:
        detect_shared_link(webdriver, link, expect_working=False)

    time.sleep(2)
    sdk.delete('/image.png')


def test_password_link(server_def, workspace, webdriver):
    sdk = PydioSdk(server_def['host'], workspace['id'], unicode(''), '', (server_def['user'], server_def['pass']))

    password = 'P@ssw0rd'
    sdk.upload(local='resources/image.png', local_stat=local_stat('resources/image.png'), path=unicode('/image.png'))
    link = sdk.share(ws_label='Shared File', ws_description='Description', password=password, expiration='', downloads='',
                     can_read='true', can_download='true', paths=u'/image.png', link_handler='', can_write='false')

    assert detect_password_share_and_submit(webdriver, link, password)

    sdk.unshare(u'/image.png')
    sdk.delete('/image.png')


def test_limited_downloads_link(server_def, workspace, webdriver):
    sdk = PydioSdk(server_def['host'], workspace['id'], unicode(''), '', (server_def['user'], server_def['pass']))

    dl_limits = 3
    sdk.upload(local='resources/image.png', local_stat=local_stat('resources/image.png'), path=unicode('/image.png'))
    link = sdk.share(ws_label='Shared File', ws_description='Description', password='', expiration='', downloads=dl_limits,
                     can_read='true', can_download='true', paths=u'/image.png', link_handler='', can_write='false')

    detect_shared_link(webdriver, link, expect_working=True, preview=True, download=True, trigger_download=dl_limits)
    # Downloads should now be expired
    detect_shared_link(webdriver, link, expect_working=False, preview=True, download=True)

    sdk.unshare(u'/image.png')
    sdk.delete('/image.png')


def test_share_move(server_def, workspace, webdriver):
    sdk = PydioSdk(server_def['host'], workspace['id'], unicode(''), '', (server_def['user'], server_def['pass']))

    # Upload and create link
    sdk.bulk_mkdir([u'/folder', u'/répertoire', u'/répertoire/content', u'/répertoire/content/link'])
    sdk.upload(local='resources/image.png', local_stat=local_stat('resources/image.png'), path=unicode('/folder/image.png'))
    link = sdk.share(ws_label='Shared File', ws_description='Description', password='', expiration='', downloads='',
                     can_read='true', can_download='true', paths=u'/folder/image.png', link_handler='', can_write='false')
    detect_shared_link(webdriver, link, expect_working=True, preview=True, download=True)
    loaded_link = check_shared_element_data(sdk, u'/folder/image.png')
    assert loaded_link == link

    # Now move original and check link is still ok
    sdk.rename('/folder/image.png', '/folder/image2.png')
    detect_shared_link(webdriver, link, expect_working=True, preview=True, download=True)
    loaded_link = check_shared_element_data(sdk, u'/folder/image2.png')
    assert loaded_link == link

    # Move to another folder
    sdk.rename('/folder/image2.png', u'/répertoire/content/link/image2.png')
    detect_shared_link(webdriver, link, expect_working=True, preview=True, download=True)
    loaded_link = check_shared_element_data(sdk, u'/répertoire/content/link/image2.png')
    assert loaded_link == link

    # Rename a parent folder
    sdk.rename(u'/répertoire/content', u'/répertoire/contenu renommé')
    detect_shared_link(webdriver, link, expect_working=True, preview=True, download=True)
    loaded_link = check_shared_element_data(sdk, u'/répertoire/contenu renommé/link/image2.png')
    assert loaded_link == link

    # Unshare. At first pass, detect correctly unshared.
    sdk.unshare(u'/répertoire/contenu renommé/link/image2.png')
    sdk.delete(u'/répertoire/contenu renommé/link/image2.png')
    sdk.delete(u'/répertoire')
    sdk.delete(u'/folder')