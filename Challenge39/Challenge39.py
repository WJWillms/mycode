#!/usr/bin/env python3
# A program that prompts a user for two operators and operation (plus or minus)
# the program then shows the result.
# The user may enter q to exit the program.

def main():
    calc1 = 0.0
    calc2 = 0.0
    operation = ""
    while (calc1 != "q" and calc2 !="q"):
        print("\nWhat is the first operator? Or, enter q to quit: ")
        calc1 = input()
        if calc1.lower() == "q":
            calc1=calc1.lower()
            break
            
        if calc1.isdigit():
            calc1 = float(calc1)
        print("\nWhat is the second operator? Or, enter q to quit: ")
        calc2 = input()
        if calc2.lower() == "q":
            calc2=calc2.lower()

            break
        if calc2.isdigit():
            calc2 = float(calc2)
        print("Enter an operation to perform on the two operators (+ or -): ")
        operation = input()
        if operation == "+":
            print("\n" + str(calc1) + " + " + str(calc2) + " = " + str(calc1 + calc2))
        elif operation == '-':
            print("\n" + str(calc1) + " - " + str(calc2) + " = " + str(calc1 - calc2))
        else:
            print("\n Not a valid entry. Restarting...")

if __name__ == '__main__':
    main()