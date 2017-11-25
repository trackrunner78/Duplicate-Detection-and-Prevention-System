import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
import os, sys
import hashlib

class Scroll(object):

    def __init__(self):
        self.root = tk.Tk()

    # create a Text widget with a Scrollbar attached
        self.txt = ScrolledText(self.root, undo=True)
        self.txt['font'] = ('consolas', '12')
        self.txt.pack(expand=True, fill='both')

class GUI:

    def __init__(self, master):
       frame = Frame(master)
       frame.pack()


       self.menuButton = Button(frame, text="Menu", height=5, width=10)
       self.menuButton.grid(row=0, sticky=W)

       self.fileButton = Button(frame, text="Files", height=5, width=10)
       self.fileButton.grid(row=1, sticky=W)

       self.dupButton = Button(frame, text="Duplicates", height=5, width=10)
       self.dupButton.grid(row=2, sticky=W)

       self.setButton = Button(frame, text="Settings", height=5, width=10)
       self.setButton.grid(row=3, sticky=W)

       self.scanButton = Button(frame, text="Scan", bg="blue", fg="white", height=3,
                                width=15)
       self.scanButton.grid(row=3, column=5, sticky=E)

       self.dupLabel = Label(frame, text="Duplicates: ")
       self.dupLabel.grid(row=2, column=3, sticky=W)
       
class Hash:
    def findDup(parentFolder):
        dups = {}
        for dirName, subdirs, fileList in os.walk(parentFolder):
            print('Scanning %s...' % dirName)
            for filename in fileList:
                path = os.path.join(dirName, filename)
                file_hash = Hash.hashfile(path)
                if file_hash in dups:
                    dups[file_hash].append(path)
                else:
                    dups[file_hash] = [path]
        return dups
 
 
    def joinDicts(dict1, dict2):
        for key in dict2.keys():
            if key in dict1:
                dict1[key] = dict1[key] + dict2[key]
            else:
                dict1[key] = dict2[key]
 
 
    def hashfile(path, blocksize = 65536):
        afile = open(path, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.hexdigest()
 
 
    def printResults(dict1):
        results = list(filter(lambda x: len(x) > 1, dict1.values()))
        if len(results) > 0:
            messagebox.showinfo("DDPS", "Duplicates Found!")
            print('The following files are identical. The name could differ, but the content is identical')
            print('___________________')
            for result in results:
                for subresult in result:
                    print('\t\t%s' % subresult)
                print('___________________')
 
        else:
            messagebox.showerror("DDPS", "No duplicate files found.")


def Scan():
    folder = filedialog.askdirectory()
    dups = {}
    folders = [folder]
    for i in folders:
        if os.path.exists(i):
            Hash.joinDicts(dups, Hash.findDup(i))
    Hash.printResults(dups)
    
def main():
    result = messagebox.askyesno("DDPS","Would you like to perform another scan?")
    if result == True:
        Scan()
    else:
        sys.exit()
    main()
            
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    result = messagebox.askyesno("DDPS","Would you like to perform a scan?")
    if result == True:
        Scan()
    else:
        sys.exit()
    main()

