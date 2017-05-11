import hashlib
import time

"""
Use to benchmark how long it takes to md5 hash directories in Python
"""
def hashfile(afile, hasher=hashlib.md5(), blocksize=65536):
    ts = time.time()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    #logging.info(" HASHED " + str(afile) + " in " + str(time.time()-ts) + "s")
    return hasher.hexdigest()

"""
# Sample usage
with open('banzai', 'r') as f:
    print(hashfile(f))
"""
