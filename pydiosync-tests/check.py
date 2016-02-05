# -*- coding: utf-8 -*-  
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

# Use this to check the status of a PydioSync task with your local FS

from watchdog.utils.dirsnapshot import DirectorySnapshot as dirsnapshot, DirectorySnapshotDiff
import pickle
import argparse

def difffolders(fld_a, fld_b):
    """ 
        :fld_a first folder to be compared
        <b>:fld_b:</b> second folder to be compared
        :return: a watchdog diff of folders
    """
    return DirectorySnapshotDiff(dirsnapshot(fld_a), dirsnapshot(fld_b))

def getReport(diff):
    report = "Directoryies created\n"
    for i in diff.dirs_created:
        report += str(i) + "\n"
    report += "\nDirectoryies deleted\n"
    for i in diff.dirs_deleted:
        report += str(i) + "\n"
    report += "\nDirectoryies modified\n"
    for i in diff.dirs_modified:
        report += str(i) + "\n"
    report += "\nDirectoryies moved\n"
    for i in diff.dirs_moved:
        report += str(i) + "\n"
    report += "\nFiles created\n"
    for i in diff.files_created:
         report += str(i) + "\n"
    report += "\nFiles deleted\n"
    for i in diff.files_deleted:
        report += str(i) + "\n"
    report += "\nFiles modified\n"
    for i in diff.files_modified:
        report += str(i) + "\n"
    report += "\nFiles moved\n"
    for i in diff.files_moved:
        report += str(i) + "\n" 
    return report

def dosnapshot(folder):
    """
    Takes a snapshot of a folder
    """
    return dirsnapshot(folder)

def savesnapshot(snapshot, filename="distant.pickle"):
    """
    Saves a pickle of snapshot
    """
    with open(filename, "wb") as f:
        pickle.dump(snapshot, f, pickle.HIGHEST_PROTOCOL)

def loadsnapshot(filename="distant.pickle"):
    """
    Returns a watchdog dirsnapshot from a pickle file
    """
    with open(filename, 'rb') as f:
        distant_snap = pickle.load(f)
    return distant_snap

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', help="Mode (d)istant | (L)ocal | (f)older diff", default='local')
    parser.add_argument('--path', help="Folder to snapshot or compare", default=".")
    parser.add_argument('--file', '-f', help="Path to distant.pickle fiel to compare the folder to", default="distant.pickle")
    args = parser.parse_args()
    if args.mode[0].lower() == 'l':
        print("Comparing " + args.path + " with distant.pickle")
        with open(args.file, 'rb') as f:
            distant_snap = pickle.load(f)
            local_snap = dirsnapshot(args.path)
            diff = DirectorySnapshotDiff(local_snap, distant_snap)
            report = getReport(diff)
            print(report)
    elif args.mode[0].lower() == 'd':
        print("Taking a snapshot of {0}, for later comparison".format(args.path))
        snapshot = dirsnapshot(args.path)
        with open("distant.pickle", "wb") as f:
            pickle.dump(snapshot, f, pickle.HIGHEST_PROTOCOL)
    elif args.mode[0].lower() == 'f':
        print("Diff mode")
        fld_a = input("Folder A:")
        fld_b = input("Folder B:")
        print(getReport(difffolders(fld_a, fld_b)))

