import humanize
import os
import requests
import sys
import time
sys.path.append('..')
from sdk.remote import PydioSdk

"""
This is a stub file meant to test upload speeds.
The point was to compare the speed of the chunked upload with Pydio vs. bare bone PHP
"""

if sys.version_info[0] > 2:
    print("Intended to be run with python2")
    print("Remember to cd ../sdk && git branch python2")
    exit(-1)

# ----------------------------------------------------------------------------
SERVER="http://192.168.0.49/"
user="pydio"
password="pydiopassword"
# ----------------------------------------------------------------------------

pydio = PydioSdk(SERVER, "uploads", "/", '', auth=(user, password), skip_ssl_verify=True)
def uploadfile(pydiosdk, fullpath, dest_name):
    rstats = os.stat(fullpath)
    fstats = {'size': rstats.st_size}
    pydiosdk.upload(fullpath, fstats, dest_name)

def sdktest():
    print("Running upload test with SDK")
    for f in ["lefile100", "lefile500", "lefile1000"]:
        ts = time.time()
        fullpath = "/Users/thomas/Pydio/tests/" + f
        uploadfile(pydio, fullpath, unicode(f))
        print(" Took " + str(time.time()-ts) + " seconds to upload " + f + " " + humanize.naturalsize(os.path.getsize(fullpath)))


def simplePost():
    print("Running upload simple test with plain request.post")
    for f in ["lefile100", "lefile500", "lefile1000"]:
        ts = time.time()
        fullpath = "/Users/thomas/Pydio/tests/" + f
        files = {'file': (f, open(fullpath).read())}
        r = requests.post(os.path.join(SERVER, "upload.php"), files=files)
        #print(r.text)
        print(" Took " + str(time.time()-ts) + " seconds to upload " + f + " " + humanize.naturalsize(os.path.getsize(fullpath)))

if __name__ == "__main__":
    uploadfile(pydio, os.path.abspath("upload.py"), unicode("upload.py"))
    """
    simplePost()
    sdktest()
    simplePost()
    sdktest()
    """

"""
Corresponding PHP script
<?php
$updir = "/var/lib/pydio/LOLupload/";
$uploadfile = $updir.basename($_FILES['file']['name']);
if(move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile)){
        echo "File processed succesfully\n";
} else {
        echo "F A I L\n";
}
echo "FILES\n";
print_r($_FILES);
echo "POST\n";
print_r($_POST);
echo "GET\n";
print_r($_GET);
echo "\n";
?>
"""
