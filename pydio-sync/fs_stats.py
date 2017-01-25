import os

"""
List a folder and finds min, max, average filesize
"""
def walk(fld):
    def w(fld, lemin, lemax, size):
        fldsize = 0
        nodes = os.listdir(fld)
        countfiles = len(nodes)
        for f in nodes:
            if os.path.isfile(f):
                s = os.path.getsize(f)
                if s < lemin or lemin == 0:
                    lemin = s
                if s > lemax or lemax == 0:
                    lemax = s
                fldsize += s
            else:
                countfiles -= 1
        return [lemin, lemax, fldsize/countfiles, countfiles]
    lemin, lemax, avgsize, countfiles = w(fld, 0, 0, 0)
    for f in os.path.listdir(fld):
        if os.path.isdir(f):
            r = walk(fld, lemin, lemax, countfiles)
            if lemin != 0 and lemin > r[0]:
                lemin = r[0]
            if lemax != 0 and lemax < r[1]:
                lemax = r[1]
            oldcount = countfiles
            countfiles += r[3]
            avgsize = oldcount/countfiles * avgsize + r[2] * r[3]/countfiles

if __name__ == "__main__":
    print("Walking fs...")

