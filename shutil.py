#!/usr/bin/env python3
import shutil
import os

def main():
    #Change directory
    os.chdir("/home/student/mycode/")
    #Copies the file
    shutil.copy("Path/To/File/FileName.txt", "/New/File/Path/Name.txt")
    #Copy an entire directory
    shutil.copytree("/Path/", "/Copied/Path")





if __name__ == '__main__':
    main()