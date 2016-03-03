# -*- coding: UTF-8 -*-
#
#  Copyright (©) 2016 Thomas Saliou - Abstrium SAS <team (at) pydio.com>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Pydio.  If not, see <http://www.gnu.org/licenses/>.
#

import os, random, time, shutil, humanize, string, math, sqlite3, re
from PIL import Image

random.seed(time.time()) # is it needed?

def randname(minsize=1):
    """ returns a random name of size > *minisze*
    """
    alpha = string.ascii_letters + " éàèàòçù" # forbidden -()$%£$€
    name = alpha[random.randint(0, len(alpha)-1)]
    while (random.random() > .25 or len(name) < minsize):
        name += alpha[random.randint(0, len(alpha)-1)]
    return name if name[0] != ' ' else name[1:]

def newfilename(filename, minsize=1, maxsize=20):
    """ Produces a new name for a file, keeps the extension
    """
    dotpos = filename.rfind('.')
    newname = randname(minsize)
    if dotpos > -1:
        return newname[:maxsize] + filename[dotpos:]
    else:
        return newname[:maxsize]

def gencopypath(filename):
    """ Create a new path name for a copy of a file, the path keeps the extension
        test.txt -> test copy.txt
    """
    maxsearch = filename.rfind('/')
    if maxsearch > -1:  # only search up to parent folder
        dotpos = filename.rfind('.', maxsearch)
        copypos = filename.rfind('copy', maxsearch)
    else:
        print("REMOVE ME?")
        dotpos = filename.rfind('.')  # probably never called
        copypos = filename.rfind('copy')
    if dotpos > -1 and copypos == -1:
        path = filename[:dotpos] + ' copy'
    elif dotpos > -1 and copypos > -1:
        path = filename[:copypos+4] 
    else:
        path = filename
    i = 0
    if dotpos > -1:
        while os.path.exists(path + str(i) + filename[dotpos:]):
            i += 1
        path = path + str(i) + filename[dotpos:]
    else:
        while os.path.exists(path + str(i)):
            i += 1
        path = path + str(i)
    return path

def lsrec(fld, depth=0):
    """ Recursive folder list
    """
    if depth <= 0:
        lsfiles = os.listdir(fld)
    else:
        lsfiles = os.listdir(fld)
        for subfolder in os.listdir(fld):
            if os.path.isdir(os.path.join(fld, subfolder)):
                lsfiles.extend([os.path.join(subfolder, sub) for sub in lsrec(os.path.join(fld, subfolder), depth-1)])
    return lsfiles

def selectrand(critfunction, fld):
    """ Randomly selects a file or folder depending on critfunction
    """
    ls = lsrec(fld, depth=3)
    maxchoice = 20
    while maxchoice > 0 and len(ls) > 0:
        maxchoice -= 1
        f = random.choice(ls)
        if critfunction(os.path.join(fld, f)):
            return os.path.join(fld, f)
    return ''

def selectrandfolder(fld):
    """ Selects a random folder within *fld*, depth=2 for now, RELATIVE path
    """
    f = selectrand(os.path.isdir, fld)
    if f.find('.DS_Store') == -1:
        return f
    else:
        return ''

def selectrandfile(fld):
    """ Randomly selects a file inside fld
    """
    # TODO use excludes
    f = selectrand(os.path.isfile, fld)
    if f.find('.DS_Store') == -1: 
        return f 
    else: 
        return ''

def selectrandfile2(fld, attempts=5):
    """ try to select a file several times
    """
    f = ""
    while attempts > 0 and f == "":
        attempts -= 1
        f = selectrandfile(fld)
    return f

def deletefolder(fld, force=False):
    if os.path.exists(fld):
        if force or input("Delete " + fld + " folder? (y)") == "y":
            shutil.rmtree(fld)

def deleterandomfolder(fld):
    """ Lists the path at folders, looks for folders, randomly selects one and deletes it
    """
    path = selectrandfolder(fld)
    #print("About to delete " + path)
    deletefolder(path, force=True)
    return path

def createfolderifnotthere(fld):
    if not os.path.exists(fld):
        os.makedirs(fld)
    if fld[-1] == "/":
        return fld[:-1]
    return fld

def listfolder(fld):
    """ returns a dictionary listing a folder recursively """
    res = dict()
    for i in os.listdir(fld):
        if os.path.isdir(os.path.join(fld, i)):
            listfolder(os.path.join(fld,i))

def createImg(name, ext=".jpg", sizex=1024, sizey=768):
    img = Image.new('RGB', (sizex, sizey), 'white')
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            #r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            a = random.randint(0,255)
            r, g, b = a, int(math.cos(a/255.0)*155), int(math.sin(a/255.0)*255)
            pixels[i, j] = (r, g, b)
    full_path = name+ext
    img.save(full_path)
    return full_path

def circleImg2(name, ext=".jpg", sizex=1024, sizey=768):
    """ Absurd full pixels brute force to check whether a pixel belongs to a cirle,
        cool result: the circle is not full"""
    img = Image.new('RGB', (sizex, sizey), 'white')
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = 50, 50, 50
            x = i - (img.size[0]/2)
            y = j - (img.size[1]/2)
            if (x*x + y*y) in [30*30, 50*50, 200*200]:
                pixels[i, j] = (130, 20, 50)
            else:
                pixels[i, j] = (r, g, b)
    full_path = name+ext
    img.save(full_path)
    return full_path

def circleImg(name, ext=".jpg", sizex=1024, sizey=768):
    """ Creates a cirle """
    img = Image.new('RGB', (sizex, sizey), 'white')
    pixels = img.load()
    inc = .5
    color = (random.randint(0, 155)+100, random.randint(0, 155)+100, random.randint(0, 155)+100)
    for i in range(math.floor(min(sizex, sizey)/10)):
        rad = random.randint(1, math.floor(min(sizex, sizey)/2-1))
        steps = 0
        while steps < 360:
            steps += inc
            x = (img.size[0]/2) + rad*math.cos(steps)
            y = (img.size[1]/2) + rad*math.sin(steps)
            pixels[x, y] = color
    full_path = name+ext
    img.save(full_path)
    return full_path

def manyfilestest(nbfiles, fld):
    """ return the size of created files """
    total = 0
    fld = createfolderifnotthere(fld)
    for i in range(nbfiles):
        full_path = fld + "/" + randname()
        f = open(full_path, 'a+')
        f.write((randname()+"\n")*SIZEFACTOR)
        while random.random() > .1:
            f.write((randname()+u"\n")*SIZEFACTOR)
        f.close()
        print("[DEBUG] written " + str(i+1) + " files")
        size = os.path.getsize(full_path)
        print("        " + humanize.naturalsize(size) + " " + full_path)
        total += size
        time.sleep(random.random()*5)
    return total

def manyimagestest(nbImages, fld):
    """ return the size of created img """
    fld = createfolderifnotthere(fld)
    total = 0
    while nbImages > 0:
        nbImages -= 1
        full_path = fld + "/" + randname(9)
        full_path = createImg(full_path, sizex=10, sizey=10)
        print("[DEBUG] created image...")
        size = os.path.getsize(full_path)
        print("        " + humanize.naturalsize(size) + " " + full_path)
        total += size
    return total

class Action:
    """ path
        [details]
        more
        info [ERROR]
    """
    def __repr__(self):
        res = ''
        if hasattr(self, 'path'):
            res = str(self.path) + "\n"
        if hasattr(self, 'details'):
            for i in self.details:
                res += " [details] " + str(self.details[i]) + "\n"
        if hasattr(self, 'more'):
            res += " [more] " + str(self.more) + "\n"
        if hasattr(self, 'info'):
            res += " [info] " + str(self.info) + "\n"
        return res

class Bot:
    """ A bot in this context is a filesystem bot, it creates, deletes, copies, moves things around in a target_fld
    """
    def __init__(self, target_fld):
        """ *target_fld* the folder in which to act
            **history** the log of bot actions
        """
        self.fld = target_fld
        self.history = {'Bot target: ' + target_fld: {time.time(): 'instanciated'}}

    def dosomething(self):
        """ Randomely do something:
            on a FOLDER or on a FILE
        """
        def logaction(action):
            """ Failed actions are not logged
            """
            if hasattr(action, "info"):
                print("  Failed  ")
                print(action.info)
            elif hasattr(action, "path"):
                if action.path in self.history:
                    self.history[action.path].append(action.details)
                else:
                    self.history[action.path] = [action.details]
        if random.random() < .3:  # folder
            action = self.dorandomfolderaction()
            logaction(action)
        else:  # file
            action = self.dorandomfileaction()
            logaction(action)
        return action

    def dosomethings(self, nbthings=2, wait=1):
        """ Do actions in the fld with with the specified delay
            :nbthings: the number of actions to do
            :wait: default is to wait for 1 second
        """
        print("Estimated run time: " + humanize.naturaltime(str(nbthings*wait))[:-4])
        for i in range(0, nbthings):
            self.dosomething()
            time.sleep(wait)

    def dorandomfolderaction(self):
        """ Folders : CREATE, DELETE, COPY, MOVE, RENAME
            TODO: refactor me with Exceptions and closures
        """
        action = Action()
        task = random.choice(['CREATE', 'DELETE', 'COPY', 'MOVE', 'RENAME'])
        if len(os.listdir(self.fld)) <= 5:
            task = 'CREATE'
        if task == 'CREATE':
            action.path = os.path.join(self.fld, randname(3))
            createfolderifnotthere(action.path)
        elif task == 'DELETE':
            action.path = deleterandomfolder(self.fld)
        elif task == 'COPY':
            randfolder = selectrandfolder(self.fld)
            if randfolder == "":
                action.info = "Failed to select a random folder to copy"
            else:
                action.path = os.path.join(self.fld, randfolder)
                try:
                    randfolder = randfolder.replace(re.search(" copy\d*", randfolder).group(), '')
                except AttributeError:
                    pass
                path = os.path.join(self.fld, randfolder) + ' copy'
                i = 1
                while os.path.exists(path + str(i)):
                    i += 1
                path = path + str(i)
                shutil.copytree(action.path, path)
        elif task == 'MOVE':
            # should this be able to move things into existing folders? #TODO
            randfolder = selectrandfolder(self.fld)
            if randfolder == "":
                action.info = "Failed to select a random folder to move"
            else:
                action.path = os.path.join(self.fld, randfolder)
                path = randname(3)
                shutil.move(action.path, os.path.join(self.fld, path))
        elif task == 'RENAME':
            # should this be able to rename things to existing folders? (DELETE + MOVE) #TODO
            randfolder = selectrandfolder(self.fld)
            if randfolder == "":
                action.info = "Failed to select a random folder to rename"
            else:
                action.path = os.path.join(self.fld, randfolder)
                path = action.path + randname(3)
                shutil.move(action.path, path)

        action.details = {"at":time.time(), "did": "Folder, " + task}
        try:  # for actions that use 2 files
            action.details["more"] = path
        except NameError:
            pass
        return action

    def dorandomfileaction(self):
        """ Files : CREATE, DELETE, COPY, MOVE, MODIFY, RENAME
        """
        action = Action()
        task = random.choice(['CREATE', 'DELETE', 'COPY', 'MOVE', 'MODIFY', 'RENAME', 'MOVEANDRENAME'])
        if len(os.listdir(self.fld)) < 5:
            task = 'CREATE'
        if task == 'CREATE':
            action.path = createImg(os.path.join(self.fld, randname(3)), random.choice([".jpg", ".png", ".tiff", ".bmp"]))
        elif task == 'DELETE':
            action.path = selectrandfile2(self.fld)
            if action.path == "":
                action.info = "Failed to select a file to delete"
            else:
                os.remove(action.path)
        elif task == 'COPY':
            action.path = selectrandfile2(self.fld)
            if action.path == "":
                action.info = "Failed to select a file to copy"
            else:
                path = gencopypath(action.path)
                shutil.copy2(action.path, path)
        elif task == 'MOVE':
            action.path = selectrandfile2(self.fld)
            if action.path == "":
                action.info = "Failed to select a file to move"
            else:
                path = selectrandfolder(self.fld)
                if path != '':
                    if os.path.isfile(path):
                        os.unlink(path)
                        time.sleep(.500)
                    shutil.move(action.path, path)
        elif task == 'RENAME':
            action.path = selectrandfile2(self.fld)
            if action.path == "":
                action.info = "Failed to select a file to rename"
            else:
                path = os.path.join(self.fld, newfilename(action.path, 3, 50))
                shutil.move(action.path, path)
        elif task == 'MOVEANDRENAME':
            action.path = selectrandfile2(self.fld)
            if action.path == "":
                action.info = "Failed to select a file to rename"
            else:
                randfld = selectrandfolder(self.fld)
                path = os.path.join(self.fld, randfld, newfilename(action.path, 3, 50))
                shutil.move(action.path, path)
        elif task == 'MODIFY':
            action.path = selectrandfile2(self.fld)
            if action.path == "":
                action.info = "Failed to select a file to modify"
            else:
                with open(action.path, 'wb') as f:
                    f.write((random.choice(['a', 'b', 'c'])*random.randint(100, 10000)).encode('utf-8'))
        action.details = {"at": time.time(), "did": "File, " + task}
        try:  # for actions that use 2 files
            action.details["more"] = path
        except NameError:
            pass
        return action

    def savehistory(dbname):
        """ writes the history to a DB for sorting and shit
        """
        db = sqlite3.connect(dbname)
        # create table actions if not exists (id PRIMARY KEY, time DATE, node TEXT, node_new TEXT)
        #for i in self.history:
            #stm = "insert into actions (time, node, node_new, info) values ({0}, {1}, {2}, {3})".format(self.history[i], self.history[i][
            #db.execute(stm)
        db.commit()
        db.close()

    def __repr__(self):
        res = ''
        for i in self.history:
            res += i
            for l in self.history[i]:
                res += "\n " + str(l)
            res += "\n"
        return res
# end of Bot

def dostuff(nbfiles):
    lefld = randname(20)
    path = "/Users/thomas/Pydio/tests/nobinnolucene1000"
    createfolderifnotthere(os.path.join(path, lefld))
    def manycirclestest(nbImages, fld):
        """ return the size of created stuff """
        fld = createfolderifnotthere(fld)
        total = 0
        while nbImages > 0:
            nbImages -= 1
            full_path = fld + "/" + randname(9)
            full_path = circleImg(full_path, sizex=50, sizey=40)
            print("[DEBUG] created image...")
            size = os.path.getsize(full_path)
            print("        " + humanize.naturalsize(size) + " " + full_path)
            total += size
        return total
    files = 10
    created_files, created_size = 0, 0
    for i in range(math.ceil(nbfiles*.1)):
        created_files += files
        created_size += manycirclestest(files, os.path.join(path, lefld))
    print("Created " + str(created_files) + " with a total size of " + str(humanize.naturalsize(created_size)))

if __name__ == "__main__":
    FLD = "/Users/thomas/Pydio/tests/syncroVBox"
    NBFILES = 100
    SIZEFACTOR = 10000
    start = time.time()
    # === Scenario ===
    # create 5 folders
    # create some files
    # create 5 folders
    # move some files
    # change some files
    # delete everything
    size = 0
    #size = manyfilestest(NBFILES/2, FLD)
    size += manyimagestest(NBFILES, FLD+"/"+"images")
    finish = time.time()
    print("Done, created " + humanize.naturalsize(size) + " in " + humanize.naturaltime(finish-start)[:-4])
