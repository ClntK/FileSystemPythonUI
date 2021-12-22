"""
Program: filesys.py
Author: Clint
Provides a menu-driven tool for navigating a file system
and gathering information on files.
"""

import os, os.path

QUIT = '8'
COMMANDS = ('1', '2', '3', '4', '5', '6', '7', '8')

MENU = """1 list the current directory
2 move up
3 move down
4 numbers of files in the directory
5 size of the directory in bytes
6 search for a filename
7 view file or directory
8 quit the program
"""
import os, os.path

def main():
    while True:
        print(os.getcwd())
        print(MENU)
        command = acceptCommand()
        runCommand(command)
        if command == QUIT:
            print("Have a nice day!")
            break
def acceptCommand():
    """Inputs and returns a legitimate command number."""
    command = input("enter a number: ")
    if command in COMMANDS:
        return command
    else: 
        print("Error: command not recognized.")
        return acceptCommand()

def runCommand(command):
    """Selects and runs a command."""
    if command == '1':
        listCurrentDir(os.getcwd())
    elif command == '2':
        moveUp()
    elif command == '3':
        moveDown(os.getcwd())
    elif command == '4':
        print("The total number of files is: ", countFiles(os.getcwd()))
    elif command == '5':
        print("The total number of bytes is: ", countBytes(os.getcwd()))
    elif command == '6':
        target = input("Enter the search string: ")
        fileList = findFiles(target, os.getcwd())
        if not fileList:
            print("String not found")
        else:
            for f in fileList:
                print(f)
    elif command == '7':
        print("Now viewing the contents of your selection.")
        displayFiles(os.getcwd())

def listCurrentDir(dirName):
    """Print a list of the cwd's contents."""
    lyst = os.listdir(dirName)
    for element in lyst: 
        print(element)

def moveUp():
    """Moves up to the parent directory."""
    os.chdir("..")

def moveDown(currentDir):
    """Moves down to the named subdirectory if it exists."""
    newDir = input("Enter the directory name: ")
    if os.path.exists(currentDir + os.sep + newDir) and os.path.isdir(newDir):
        os.chdir(newDir)
    else:
        print("ERROR: no such name.")

def countFiles(path):
    """Returns athe number of files in the cwd 
    and all its subdirectories."""
    count = 0
    lyst = os.listdir(path)
    for element in lyst:
        if os.path.isfile(element):
            count += 1
        else: 
            os.chdir(element)
            count += countFiles(os.getcwd())
            os.chdir("..")
    return count

def countBytes(path):
    """Returns the number of bytes in the cwd and
    all its subdirectories."""
    count = 0
    lyst = os.listdir(path)
    for element in lyst:
        if os.path.isfile(element):
            count += os.path.getsize(element)
        else:
            os.chdir(element)
            count += countBytes(os.getcwd())
            os.chdir("..")
    return count

def findFiles(target, path):
    """Returns a list of the filenames that contain
    the target string in the cwd and all its subdirectories."""
    files = []
    lyst = os.listdir(path)
    #print(lyst)
    for element in lyst:
        if os.path.isfile(element):
            if target in element:
                files.append(path + os.sep + element)
            elif os.path.isdir(element):                
                os.chdir(element)
                files.extend(findFiles(target, os.getcwd()))
                os.chdir("..")
    return files 

def displayFiles(path):    
    """Visits all of the files and directories in
        path and displays the files' contents."""    
    if os.path.isfile(path):        
        print("File name: " + path)        
        f = open(path, 'r')        
        print(f.read())    
    else:        
        print("Directory name: " + path)        
        lyst = os.listdir(path)        
        for element in lyst:            
            displayFiles(path+"/"+element)

if __name__ == "__main__":
    main()