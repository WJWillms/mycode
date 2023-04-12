#!/usr/bin/env python3


def main():
    round = 0
    answer = ""

    while round < 3 and answer != "Brian":
        round += 1     
        answer = input('Finish the movie title, "Monty Python\'s The Life of ______": ')
        if answer.lower() == "brian": 
            print("Correct!")
            answer = answer.title()
        elif round == 3:    
            print("Sorry, the answer was Brian.")
        else:                 
            print("Sorry. Try again!")

if __name__ == '__main__':
    main()