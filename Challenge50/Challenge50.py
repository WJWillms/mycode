#!/usr/bin/env python3


def main():
    vampCounter = 0
    with open("/home/student/mycode/Challenge50/dracula.txt", "r") as novel:
        with open("vampytimes.txt", "w") as vampire:
            for line in novel:
                if "vampire"  in line.lower():
                    vampCounter += 1
                    vampire.write(line)
    print("Amount of lines with Vampire: " + str(vampCounter))
if __name__ == '__main__':
    main()