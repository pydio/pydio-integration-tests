# pydio-automated-integration-tests
Tools for automatically testing various aspects of a deployed Pydio instance.

# How-to Run
Install PyTest (see pytest.org)
Run py.test in root folder, or python main.py in root folder

# Installing selenium & firefox for UI tests
On Debian 8, install firefox: 
Add `deb http://packages.linuxmint.com debian import` to the sources.list  

```sudo apt-get install xvfb firefox libasound2 libdbus-glib-1-dev```

Install selenium  
`pip install selenium`

Launch Xvfb Server
`nohup Xvfb :10 -ac &`

# Before running tests
`export DISPLAY=:10`

