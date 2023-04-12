#!/usr/bin/env python3
import os
import time
import termios
import sys
import tty
import random

def greeter():
    clearscreen()
    message = "Welcome to Rock Paper Scissors. The objective of the game is to beat your opponent by choosing the card that will beat your opponents.\nRock beats Scissors, Scissors beats Paper, and Paper beats Rock.\nYou have 5 of each card.You win by beating your opponent 3 times, you lose if your opponent wins 3 times, and draw if you run out of cards.\nPress any button to begin!"
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.04)
    keypress()
    clearscreen()
    
def clearscreen():
    print("\033c")

def keypress():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def cardChoice(Cards):
    validCard=False
    while validCard == False:
        print("What card would you like to play?")
        print("1. Rock (You have " + str(Cards[0]) + " cards left)")
        print("2. Paper (You have " + str(Cards[1]) + " cards left)")
        print("3. Scissors (You have " + str(Cards[2]) + " cards left)")
        card = (input("Choice: "))
        
        try:
            card = int(card)
        except ValueError:
            print("Invalid Choice")
            time.sleep(1)
            clearscreen()

        if isinstance(card, (int)):
            
            if card > 0 and card < 4:
                if Cards[card-1] > 0:
                    clearscreen()
                    return card-1
                else:
                    print("Not enough cards of that type")
                    time.sleep(1)
                    clearscreen()
            else:
                print("Invalid Choice")
                time.sleep(1)
                clearscreen()
        else: 
            print("Invalid Choice")
            time.sleep(1)
            clearscreen()

def CPUcardChoice(Cards):
    validCard=False
    while validCard == False:
        CPUchoice = random.randint(0,2)
        if Cards[CPUchoice] > 0:
            return CPUchoice

def Battle(user, CPU):
    print("Opponents Card")
    print("-----------------------------------------")
    if CPU == 0:
        RockChoice()
    elif CPU == 1:
        PaperChoice()
    elif CPU == 2:
        ScissorChoice()
    print("Your Card")
    print("-----------------------------------------")
    if user == 0:
        RockChoice()
    elif user == 1:
        PaperChoice()
    elif user == 2:
        ScissorChoice()
    print("-----------------------------------------")
    #Calculate winner return 1=user win, 2=CPU win, 3=tie
    if user == 0 and CPU == 0:
        print("The round is a Draw!")
        return 3
    elif user == 0 and CPU == 1:
        print("The CPU won the round!")
        return 2
    elif user == 0 and CPU == 2:
        print("You won the round!")
        return 1
    elif user == 1 and CPU == 0:
        print("You won the round!")
        return 1
    elif user == 1 and CPU == 1:
        print("The round is a Draw!")
        return 3
    elif user == 1 and CPU == 2:
        print("The CPU won the round!")
        return 2
    elif user == 2 and CPU == 0:
        print("The CPU won the round!")
        return 2
    elif user == 2 and CPU == 1:
        print("You won the round!")
        return 1
    elif user == 2 and CPU == 2:
        print("The round is a Draw!")
        return 3
    
           
def PaperChoice():
    print("""
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
""")

def RockChoice():
    print("""
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
""")

def ScissorChoice():
    print("""
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
""")

def LifeUpdate(user,CPU,cards):
    print("CPU Lives: " + str(CPU))
    print("Your Lives: " + str(user))
    print(str(cards) + " cards remain to be played")
    print("Press any button to proceed to the next round")
    keypress()
    clearscreen()

def main():
    #Numbers in list coordinate to Rock, Paper, Scissors(Respectively) and the amount of that card that is left
    
    greeter()
    again = True
    while again == True:
        user_Cards = [5,5,5]
        CPU_Cards = [5,5,5]
        Card_Count = 15
        user_Lives = 3
        CPU_Lives = 3
        gameContinue = True
        while gameContinue == True:    
            #Getting User Card
            user_Choice = cardChoice(user_Cards) 
            #Getting CPU Card
            CPU_Choice = CPUcardChoice(CPU_Cards)
            #Calc Winner
            winner = Battle(user_Choice, CPU_Choice)
            if winner == 1:
                CPU_Lives -= 1
            elif winner == 2:
                user_Lives -= 1

            #Updating list/card values
            user_Cards[user_Choice] -= 1
            CPU_Cards[CPU_Choice] -= 1
            Card_Count -= 1
            time.sleep(2)
            clearscreen()
            if user_Lives == 0:
                gameContinue = False
                x = input("The CPU won " + str(CPU_Lives) + " to " + str(user_Lives) +". Enter 1 to play again or anything else to quit: ")
                if x != '1':
                    again = False
                clearscreen()
            elif CPU_Lives == 0:
                gameContinue = False
                x = input("You won " + str(user_Lives) + " to " + str(CPU_Lives) +". Enter 1 to play again or anything else to quit: ")
                if x != '1':
                    again = False
                clearscreen()
            elif user_Lives > 0 and CPU_Lives > 0 and Card_Count == 0:
                gameContinue = False
                x= input(print("Out of cards. The game is a draw. Enter 1 to play again or anything else to quit: "))
                clearscreen()
            if user_Lives > 0 and CPU_Lives > 0 and Card_Count > 0:
                LifeUpdate(user_Lives, CPU_Lives, Card_Count)




    
    

if __name__ == '__main__':
    main()