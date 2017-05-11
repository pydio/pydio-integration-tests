import os, random, subprocess, time

"""
Get a visual representation of a folder, can be useful to find out if the directory tree is wide
Note: using the command tree can be more useful
"""

def folder2dot(fld):
    nodes = os.listdir(fld)
    res = ""
    for f in nodes:
        if os.path.isdir(os.path.join(fld, f)):
            res += "node [style=filled, color=" + random.choice(['red', 'blue', 'yellow', 'orange', 'green']) + "];"
            res += '"' + fld + '" -- "' + os.path.join(fld, f) + '";\n'
            res += folder2dot(os.path.join(fld, f))
            res += "node [style=rounded, color=black];"
        else:
            res += '"' + fld + '" -- "' + f + '";\n'
    return res

if __name__ == "__main__":
    dot = "graph legraph {\n"
    dot += folder2dot('/Users/thomas/Pydio/tests/big')
    dot += "}\n"
    with open('testvisu.dot', 'wb') as f:
        f.write(dot.encode('utf-8'))
    cmd = "dot -Tsvg -omonImage.svg testvisu.dot"
    print(cmd)
    start = time.time()
    subprocess.check_output(cmd, shell=True)
    delta = time.time()-start
    print("Generated monImage.svg in " + str(delta) + " seconds.")
