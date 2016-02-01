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
import sys
import pydioenv

cmd = 'test'
param = ''
if len(sys.argv) > 2 :
    cmd = sys.argv[1]
    param = sys.argv[2]

if cmd == 'test':
    import pytest
    pytest.main(args=['-s'])
elif cmd == 'install':
    import json
    from sdk.remote import PydioSdk
    fname = param
    with open(fname) as serverP:
        server_data = json.load(serverP)
        sdk = PydioSdk(url=server_data['host'], skip_ssl_verify=pydioenv.noverify)
        response = sdk.install(server_data['install_data'])
        if response != 'OK':
            exit(1)
