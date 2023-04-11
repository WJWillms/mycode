#!/usr/bin/env python3
import os

def main():
    print("\033c")
    #or
    os.system('cls' if os.name == 'nt' else 'clear')
    

if __name__ == '__main__':
    main()