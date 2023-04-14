#!/usr/bin/env python3
import time

def main():
    num = -1
    while num > 100 or num < 1:
        num = int(input("Enter a number between 1 and 100: "))
    
    for x in range(num, 0, -1):
        print(str(x) + " bottles of beer on the wall!")
        print(str(x) + " bottles of beer on the wall! " + str(x) + " bottles of beer! You take one down, pass it around!")
        time.sleep(1)
        if x == 1:
            print("0 bottles of beer on the wall!")


    

if __name__ == '__main__':
    main()