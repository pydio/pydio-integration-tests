 # vim: set fileencoding=utf-8

 Copyright (©) 2015 Thomas Saliou - Abstrium SAS <team (at) pydio.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; version 2 of the License.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Pydio.  If not, see <http://www.gnu.org/licenses/>.

Set up the environment
======================

virtualenv pydio3 --python=python3.5
cd pydio3
source bin/activate
pip install -r requirements.txt

Example usage
=============
python test_interactive.py

Build the documentation
=======================
pip install -r doc/requirements.txt
cd doc
make html
