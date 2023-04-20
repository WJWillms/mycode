#!/usr/bin/env python3
import numpy as np
import random
import os
import time
import curses
import textwrap

#Types assigned to a number value for computing
# 1=Grass, 2=Fire, 3=Water, 4=Flying, 5=Electric, 6=Poison, 7=Bug, 8=Normal, 9=Ground, 10=Fairy,11=Dark 12=Fighting, 13=Psychic, 14=Rock,
#15=Steel, 16=Ice, 17=Ghost, 18=Dragon, 0=MonoType

#Type Strength/Weakness Breakdown
#Type                 Super Effective Against                                  Weak to
#Grass(1)          Ground(9), Rock(14), Water(3)                Bug(7), Fire(2), Flying(4), Ice(16), Poison(6)
#Fire(2)           Bug(7), Grass(1), Ice(16), Steel(15)                Ground(9), Rock(14), Water(3)
#Water(3)          Fire(2), Ground(9), Rock(14)                           Electric(5), Grass(1)
#Flying(4)        Bug(7), Fighting(12), Grass(1)                    Electric(5), Ice(16), Rock(14)
#Electric(5)          Flying(4), Water(3)                                     Ground(9)
#Poison(6)            Fairy(10), Grass(1)                              Ground(9), Psychic(13)
#Bug(7)          Dark(11), Grass(1), Psychic(13)                       Fire(2), Flying(4), Rock(14)
#Normal(8)                   N/A                                             Fighting(12)
#Ground(9)   Electric(5), Fire(2), Poison(6), Rock(14), Steel(15)     Grass(1), Ice(16), Water(3)
#Fairy(10)          Dark(11), Dragon(18), Fighting(12)                      Poison(6), Steel(15)
#Dark(11)               Ghost(17), Psychic(13)                          Bug(7), Fairy(10), Fighting(12)
#Fighting(12)  Dark(11), Ice(16), Normal(8), Rock(14), Steel(15)        Fairy(10), Flying(4), Psychic(13)
#Pyschic(13)            Fighting(12), Poison(6)                         Bug(7), Dark(11), Ghost(17)
#Rock(14)         Fire(2), Flying(4), Ice(16), Bug(7)         Fighting(12), Grass(1), Ground(9), Steel(15), Water(3)
#Steel(15)            Fairy(10), Ice(16), Rock(14)                   Fighting(12), Fire(2), Ground(9)
#Ice(16)       Dragon(18), Flying(4), Grass(1), Ground(9)         Fighting(12), Fire(2), Rock(14), Steel(15)
#Ghost(17)              Ghost(17), Psychic(13)                              Dark(11), Ghost(17)
#Dragon(18)                 Dragon(18)                               Dragon(18), Fairy(10), Ice(16)

#Move Categories 1 = Physical, 2 = Special, 3 = Non-Damaging

"""Future Key Press
import msvcrt

while True:
    key = msvcrt.getch()
    if key.isdigit() and int(key) in range(1, 5):
        num = int(key)
        break
    else:
        print("Invalid input. Please try again.")

print("You pressed", num)
"""

def greeter(stdscr):
        # Turn off cursor visibility
    curses.curs_set(0)

    # Set up colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Define logo and message strings
    logo = r'''
          ,'\  
_.----.        ____         ,'  _\___    ___    ____
,-'       `.     |    |  /`.   \,-'    |   \  /   |   |    \  |`.
\      __    \    '-.  | /   `.  ___    |    \/    |   '-.   \ |  |
 \.    \ \   |  __  |  |/    ,','_  `.  |          | __  |    \|  |
   \    \/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |
    \     ,-'/  /   \    ,'   | \/ / ,`.|         /  /   \  |     |
     \    \ |   \_/  |   `-.  \    `'  /|  |    ||   \_/  | |\    |
      \    \ \      /       `-.`.___,-' |  |\  /| \      /  | |   |
       \    \ `.__,'|  |`-._    `|      |__| \/ |  `.__,'|  | |   |
        \_.-'       |__|    `-._ |              '-.|     '-.| |   |
                                `'                            '-._|
'''
    logo_lines = textwrap.wrap(logo, curses.COLS)
    message = "Press any key to continue"

    # Get dimensions of logo and message strings
    logo_rows, logo_cols = logo.split('\n')[1:-1], max(map(len, logo.split('\n')))
    message_rows, message_cols = message.count('\n') + 1, len(message)

    # Calculate center coordinates
    center_y, center_x = curses.LINES // 2, curses.COLS // 2
    logo_y = center_y - (len(logo_rows) // 2)
    message_y = center_y + (len(logo_rows) // 2) + 1

    # Display logo
    for i, row in enumerate(logo_rows):
        stdscr.addstr(logo_y+i, center_x-(len(row) // 2), row, curses.color_pair(1))

    # Fade in message
    for i in range(255):
        stdscr.addstr(message_y, center_x-(message_cols // 2), message, curses.color_pair(2) | curses.A_BOLD | curses.A_BLINK)
        stdscr.refresh()
        curses.napms(10)


    # Wait for user input
    while True:
        c = stdscr.getch()
        if c != curses.ERR:
            break

    # Restore cursor visibility
    curses.curs_set(1)


    


    

def clearscreen():
    print("\033c")

#Grabs cpu pokemon stats
def CPUChoice():
    num = 0#random.randint(0,0)
    pokemon_DB = ["Venusaur.txt"]
    text = pokemon_DB[num]
    configfile = open(text, "r")
    party_Pokemon = []
    for pokemon in configfile: 
        pokemon = pokemon.strip()
        try:
            pokemon = int(pokemon)
        except ValueError:
# Handle the case where the line is not an integer
            pokemon = pokemon.strip()
        party_Pokemon.append(pokemon)
    configfile.close()
    
    return party_Pokemon

#Grabs the text file for stats
def StatDB(num):
    pokemon_DB = ["Venusaur.txt"]
    num = pokemon_DB[num-1]
    configfile = open(num, "r")
    party_Pokemon = []
    for pokemon in configfile: 
        pokemon = pokemon.strip()
        try:
            pokemon = int(pokemon)
        except ValueError:
# Handle the case where the line is not an integer
            pokemon = pokemon.strip()
        party_Pokemon.append(pokemon)
    configfile.close()
    return party_Pokemon

def asciiRead(player,cpu):
    asciiDB = ["VenusaurAscii.txt"]
    cpuAsciiDB = ["VenusaurAsciiCpu.txt"]
    playerAscii = asciiDB[player]
    cpuAscii = cpuAsciiDB[cpu]
    with open(playerAscii, 'r') as file1, open(cpuAscii, 'r') as file2:
        for line1, line2 in zip(file1, file2):
            print(line1.rstrip(), line2.rstrip())
    

def AtkBaseDamage(attacker, defender, move):

    #(((2 * 100 / 5 + 2) * Move_Power * attackstat / defensestat) /50 + 2)
    if move == 1:
        if attacker[13] == 1:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[14] * attacker[3] / defender[5]) /50 + 2)
        elif attacker[13] == 2:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[14] * attacker[4] / defender[6]) /50 + 2)
        else:
            print("Run non damaging attack")
    if move == 2:
        if attacker[22] == 1:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[23] * attacker[3] / defender[5]) /50 + 2)
        elif attacker[22] == 2:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[23] * attacker[4] / defender[6]) /50 + 2)
        else:
            print("Run non damaging attack")
    if move == 3:
        if attacker[31] == 1:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[32] * attacker[3] / defender[5]) /50 + 2)
        elif attacker[31] == 2:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[32] * attacker[4] / defender[6]) /50 + 2)
        else:
            print("Run non damaging attack")
    if move == 4:
        if attacker[40] == 1:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[41] * attacker[3] / defender[5]) /50 + 2)
        elif attacker[40] == 2:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[41] * attacker[4] / defender[6]) /50 + 2)
        else:
            print("Run non damaging attack")
    return baseDamage

def typeCalc(atkType, defTypeOne, defTypeTwo):
    modifier = 1.0
    if atkType == 1:
        if (defTypeOne == 9) or \
            (defTypeOne == 14) or \
            (defTypeOne == 3):
                modifier = modifier * 2
        elif (defTypeOne == 7) or \
            (defTypeOne == 2) or \
            (defTypeOne == 16) or \
            (defTypeOne == 6) or \
            (defTypeOne == 14):
                modifier = modifier * 0.5
    elif atkType == 2:
        if (defTypeOne == 1) or \
            (defTypeOne == 7) or \
            (defTypeOne == 15) or \
            (defTypeOne == 16):
                modifier = modifier * 2
        elif (defTypeOne == 3) or \
            (defTypeOne == 9) or \
            (defTypeOne == 14):
                modifier = modifier * 0.5
    elif atkType == 3:
        if (defTypeOne == 2) or \
            (defTypeOne == 9) or \
            (defTypeOne == 14):
                modifier = modifier * 2
        elif (defTypeOne == 1) or \
            (defTypeOne == 5):
                modifier = modifier * 0.5
    elif atkType == 4:
        if (defTypeOne == 1) or \
            (defTypeOne == 7) or \
            (defTypeOne == 12):
                modifier = modifier * 2
        elif (defTypeOne == 5) or \
            (defTypeOne == 14) or \
            (defTypeOne == 16):
                modifier = modifier * 0.5
    elif atkType == 5:
        if (defTypeOne == 4) or \
            (defTypeOne == 3):
                modifier = modifier * 2
        elif (defTypeOne == 9):
            modifier = modifier * 0.5
    elif atkType == 6:
        if (defTypeOne == 10) or \
            (defTypeOne == 1):
                modifier = modifier * 2
        elif (defTypeOne == 6) or \
            (defTypeOne == 9) or \
            (defTypeOne == 13):
                modifier = modifier * 0.5
    elif atkType == 7:
        if (defTypeOne == 1) or \
            (defTypeOne == 11) or \
            (defTypeOne == 13):
                modifier = modifier * 2
        elif (defTypeOne == 2) or \
            (defTypeOne == 4) or \
            (defTypeOne == 14):
                modifier = modifier * 0.5
    elif atkType == 8:
        if (defTypeOne == 12):
            modifier = modifier * 0.5
    elif atkType == 9:
        if (defTypeOne == 2) or \
            (defTypeOne == 5) or \
            (defTypeOne == 5) or \
            (defTypeOne == 5) or \
            (defTypeOne == 6):
                modifier = modifier * 2
        elif (defTypeOne == 1) or \
            (defTypeOne == 3) or \
            (defTypeOne == 16):
                modifier = modifier * 0.5
    elif atkType == 10:
        if (defTypeOne == 11) or \
            (defTypeOne == 12) or \
            (defTypeOne == 18):
             modifier = modifier * 2
        elif (defTypeOne == 6) or \
            (defTypeOne == 15):
                modifier = modifier * 0.5
    elif atkType == 11:
        if (defTypeOne == 13) or \
            (defTypeOne == 17):
                modifier = modifier * 2
        elif (defTypeOne == 7) or \
            (defTypeOne == 10) or \
            (defTypeOne == 12):
                modifier = modifier * 0.5
    elif atkType == 12:
        if (defTypeOne == 8) or \
            (defTypeOne == 11) or \
            (defTypeOne == 14) or \
            (defTypeOne == 15) or \
            (defTypeOne == 16):
                modifier = modifier * 2
        elif (defTypeOne == 4) or \
            (defTypeOne == 10) or \
            (defTypeOne == 13):
                modifier = modifier * 0.5
    elif atkType == 13:
        if (defTypeOne == 6) or \
            (defTypeOne == 12):
                modifier = modifier * 2
        elif (defTypeOne == 7) or \
            (defTypeOne == 11) or \
            (defTypeOne == 17):
                modifier = modifier * 0.5
    elif atkType == 14:
        if (defTypeOne == 2) or \
            (defTypeOne == 4) or \
            (defTypeOne == 7) or \
            (defTypeOne == 16):
                modifier = modifier * 2
        elif (defTypeOne == 1) or \
            (defTypeOne == 3) or \
            (defTypeOne == 9) or \
            (defTypeOne == 12) or \
            (defTypeOne == 15):
                modifier = modifier * 0.5
    elif atkType == 15:
        if (defTypeOne == 10) or \
            (defTypeOne == 14) or \
            (defTypeOne == 16):
                modifier = modifier * 2
        elif (defTypeOne == 2) or \
            (defTypeOne == 9) or \
            (defTypeOne == 12):
                modifier = modifier * 0.5
    elif atkType == 16:
        if (defTypeOne == 1) or \
            (defTypeOne == 4) or \
            (defTypeOne == 9) or \
            (defTypeOne == 18):
                modifier = modifier * 2
        elif (defTypeOne == 2) or \
            (defTypeOne == 12) or \
            (defTypeOne == 14) or \
            (defTypeOne == 15):
                modifier = modifier * 0.5
    elif atkType == 17:
        if (defTypeOne == 13) or \
            (defTypeOne == 17):
                modifier = modifier * 2
        elif (defTypeOne == 11):
                modifier = modifier * 0.5
    elif atkType == 18:
        if (defTypeOne == 18):
                modifier = modifier * 2
        elif (defTypeOne == 10) or \
            (defTypeOne == 16):
                modifier = modifier * 0.5




    if atkType == 1:
        if (defTypeTwo == 9) or \
            (defTypeTwo == 14) or \
            (defTypeTwo == 3):
                modifier = modifier * 2
        elif (defTypeTwo == 7) or \
            (defTypeTwo == 2) or \
            (defTypeTwo == 16) or \
            (defTypeTwo == 6) or \
            (defTypeTwo == 14):
                modifier = modifier * 0.5
    elif atkType == 2:
        if (defTypeTwo == 1) or \
            (defTypeTwo == 7) or \
            (defTypeTwo == 15) or \
            (defTypeTwo == 16):
                modifier = modifier * 2
        elif (defTypeTwo == 3) or \
            (defTypeTwo == 9) or \
            (defTypeTwo == 14):
                modifier = modifier * 0.5
    elif atkType == 3:
        if (defTypeTwo == 2) or \
            (defTypeTwo == 9) or \
            (defTypeTwo == 14):
                modifier = modifier * 2
        elif (defTypeTwo == 1) or \
            (defTypeTwo == 5):
                modifier = modifier * 0.5
    elif atkType == 4:
        if (defTypeTwo == 1) or \
            (defTypeTwo == 7) or \
            (defTypeTwo == 12):
                modifier = modifier * 2
        elif (defTypeTwo == 5) or \
            (defTypeTwo == 14) or \
            (defTypeTwo == 16):
                modifier = modifier * 0.5
    elif atkType == 5:
        if (defTypeTwo == 4) or \
            (defTypeTwo == 3):
                modifier = modifier * 2
        elif (defTypeTwo == 9):
            modifier = modifier * 0.5
    elif atkType == 6:
        if (defTypeTwo == 10) or \
            (defTypeTwo == 1):
                modifier = modifier * 2
        elif (defTypeTwo == 6) or \
            (defTypeTwo == 9) or \
            (defTypeTwo == 13):
                modifier = modifier * 0.5
    elif atkType == 7:
        if (defTypeTwo == 1) or \
            (defTypeTwo == 11) or \
            (defTypeTwo == 13):
                modifier = modifier * 2
        elif (defTypeTwo == 2) or \
            (defTypeTwo == 4) or \
            (defTypeTwo == 14):
                modifier = modifier * 0.5
    elif atkType == 8:
        if (defTypeTwo == 12):
            modifier = modifier * 0.5
    elif atkType == 9:
        if (defTypeTwo == 2) or \
            (defTypeTwo == 5) or \
            (defTypeTwo == 5) or \
            (defTypeTwo == 5) or \
            (defTypeTwo == 6):
                modifier = modifier * 2
        elif (defTypeTwo == 1) or \
            (defTypeTwo == 3) or \
            (defTypeTwo == 16):
                modifier = modifier * 0.5
    elif atkType == 10:
        if (defTypeTwo == 11) or \
            (defTypeTwo == 12) or \
            (defTypeTwo == 18):
             modifier = modifier * 2
        elif (defTypeTwo == 6) or \
            (defTypeTwo == 15):
                modifier = modifier * 0.5
    elif atkType == 11:
        if (defTypeTwo == 13) or \
            (defTypeTwo == 17):
                modifier = modifier * 2
        elif (defTypeTwo == 7) or \
            (defTypeTwo == 10) or \
            (defTypeTwo == 12):
                modifier = modifier * 0.5
    elif atkType == 12:
        if (defTypeTwo == 8) or \
            (defTypeTwo == 11) or \
            (defTypeTwo == 14) or \
            (defTypeTwo == 15) or \
            (defTypeTwo == 16):
                modifier = modifier * 2
        elif (defTypeTwo == 4) or \
            (defTypeTwo == 10) or \
            (defTypeTwo == 13):
                modifier = modifier * 0.5
    elif atkType == 13:
        if (defTypeTwo == 6) or \
            (defTypeTwo == 12):
                modifier = modifier * 2
        elif (defTypeTwo == 7) or \
            (defTypeTwo == 11) or \
            (defTypeTwo == 17):
                modifier = modifier * 0.5
    elif atkType == 14:
        if (defTypeTwo == 2) or \
            (defTypeTwo == 4) or \
            (defTypeTwo == 7) or \
            (defTypeTwo == 16):
                modifier = modifier * 2
        elif (defTypeTwo == 1) or \
            (defTypeTwo == 3) or \
            (defTypeTwo == 9) or \
            (defTypeTwo == 12) or \
            (defTypeTwo == 15):
                modifier = modifier * 0.5
    elif atkType == 15:
        if (defTypeTwo == 10) or \
            (defTypeTwo == 14) or \
            (defTypeTwo == 16):
                modifier = modifier * 2
        elif (defTypeTwo == 2) or \
            (defTypeTwo == 9) or \
            (defTypeTwo == 12):
                modifier = modifier * 0.5
    elif atkType == 16:
        if (defTypeTwo == 1) or \
            (defTypeTwo == 4) or \
            (defTypeTwo == 9) or \
            (defTypeTwo == 18):
                modifier = modifier * 2
        elif (defTypeTwo == 2) or \
            (defTypeTwo == 12) or \
            (defTypeTwo == 14) or \
            (defTypeTwo == 15):
                modifier = modifier * 0.5
    elif atkType == 17:
        if (defTypeTwo == 13) or \
            (defTypeTwo == 17):
                modifier = modifier * 2
        elif (defTypeTwo == 11):
                modifier = modifier * 0.5
    elif atkType == 18:
        if (defTypeTwo == 18):
                modifier = modifier * 2
        elif (defTypeTwo == 10) or \
            (defTypeTwo == 16):
                modifier = modifier * 0.5

    return modifier

def stabBonus(moveType, typeOne, typeTwo):
    modifier = 1.0
    if moveType == typeOne or moveType == typeTwo:
        modifier = 1.5
    return modifier
    
def statsDisplay(player, cpu):
    print(player[1], end="")
    for char in range(71-len(player[1])):
          print(" ", end="")
    print("|                  |", end="")
    for char in range(79 - len(player[1]) - len(cpu[1])):
          print(" ", end="")
    print(cpu[1])

def hpDisplay(player, playerAdj, cpu, cpuAdj):
    print(str(playerAdj[2]) + "/" + str(player[2]) + "                                                                                                                                  " + str(cpuAdj[2]) + "/" + str(cpu[2]))

def moveDisplay(pokemon):
    #firstSpace and the following if else is for output blank spacing formmating
    firstSpace = True
    if len(pokemon[10]) > len(pokemon[28]):
        spaceMaker = len(pokemon[10])
        firstSpace = True
    else:
        spaceMaker = len(pokemon[28])
        firstSpace = False
    #Output moves
    print("1.)" + pokemon[10], end="")
    if firstSpace == True:
        print(" |2.)" + pokemon[19])
        print("3.)" + pokemon[28], end="")
        for char in range(spaceMaker - len(pokemon[28])):
            print(" ", end="")
        print(" |4.)" + pokemon[37])
    else:
        for char in range(spaceMaker - len(pokemon[10])):
            print(" ", end="")
        print(" |2.)" + pokemon[19])
        print("3.)" + pokemon[28] + "   |4.)" + pokemon[37])

def moveChoose(player, playerAdj, cpu, cpuAdj):
    moveChosen = False
    while moveChosen == False:  
        while True:
            print("Choose a move:", end="")
            key = input()
            if key.isdigit() and int(key) in range(1, 5):
                moveChoice = int(key)
                break
            else:
                print("Invalid input. Please try again.")
    
        if moveChoice == 1:
            clearscreen()
            asciiRead(player[0], cpu[0])
            statsDisplay(player, cpu)
            hpDisplay(player, playerAdj, cpu, cpuAdj)
            print("Move: " + player[10])
            print("Description: " + player[11])
            print("1.) Use Move")
            print("2.) Go Back")
            while True:
                num = input("Choice: ")
                if num.isdigit() and int(num) in range(1, 3):
                    num = int(num)
                    break
                else:
                    print("Invalid input. Please try again.")
                    time.sleep(.5)
                    clearscreen()
                    asciiRead(player[0], cpu[0])
                    statsDisplay(player, cpu)
                    hpDisplay(player, playerAdj, cpu, cpuAdj)
                    print("Move: " + player[10])
                    print("Description: " + player[11])
                    print("1.) Use Move")
                    print("2.) Go Back")
            if num == 1:
                return moveChoice
            else:
                clearscreen()
                asciiRead(player[0], cpu[0])
                statsDisplay(player, cpu)
                hpDisplay(player, playerAdj, cpu, cpuAdj)
                moveDisplay(player)
        elif moveChoice == 2:
            clearscreen()
            asciiRead(player[0], cpu[0])
            statsDisplay(player, cpu)
            hpDisplay(player, playerAdj, cpu, cpuAdj)
            print("Move: " + player[19])
            print("Description: " + player[20])
            print("1.) Use Move")
            print("2.) Go Back")
            while True:
                num = input("Choice: ")
                if num.isdigit() and int(num) in range(1, 3):
                    num = int(num)
                    break
                else:
                    print("Invalid input. Please try again.")
                    time.sleep(.5)
                    clearscreen()
                    asciiRead(player[0], cpu[0])
                    statsDisplay(player, cpu)
                    hpDisplay(player, playerAdj, cpu, cpuAdj)
                    print("Move: " + player[19])
                    print("Description: " + player[20])
                    print("1.) Use Move")
                    print("2.) Go Back")
            if num == 1:
                return moveChoice
            else:
                clearscreen()
                asciiRead(player[0], cpu[0])
                statsDisplay(player, cpu)
                hpDisplay(player, playerAdj, cpu, cpuAdj)
                moveDisplay(player)
        elif moveChoice == 3:
            clearscreen()
            asciiRead(player[0], cpu[0])
            statsDisplay(player, cpu)
            hpDisplay(player, playerAdj, cpu, cpuAdj)
            print("Move: " + player[28])
            print("Description: " + player[29])
            print("1.) Use Move")
            print("2.) Go Back")
            while True:
                num = input("Choice: ")
                if num.isdigit() and int(num) in range(1, 3):
                    num = int(num)
                    break
                else:
                    print("Invalid input. Please try again.")
                    time.sleep(.5)
                    clearscreen()
                    asciiRead(player[0], cpu[0])
                    statsDisplay(player, cpu)
                    hpDisplay(player, playerAdj, cpu, cpuAdj)
                    print("Move: " + player[28])
                    print("Description: " + player[29])
                    print("1.) Use Move")
                    print("2.) Go Back")
            if num == 1:
                return moveChoice
            else:
                clearscreen()
                asciiRead(player[0], cpu[0])
                statsDisplay(player, cpu)
                hpDisplay(player, playerAdj, cpu, cpuAdj)
                moveDisplay(player)
        else:
            clearscreen()
            asciiRead(player[0], cpu[0])
            statsDisplay(player, cpu)
            hpDisplay(player, playerAdj, cpu, cpuAdj)
            print("Move: " + player[37])
            print("Description: " + player[38])
            print("1.) Use Move")
            print("2.) Go Back")
            while True:
                num = input("Choice: ")
                if num.isdigit() and int(num) in range(1, 3):
                    num = int(num)
                    break
                else:
                    print("Invalid input. Please try again.")
                    time.sleep(.5)
                    clearscreen()
                    asciiRead(player[0], cpu[0])
                    statsDisplay(player, cpu)
                    hpDisplay(player, playerAdj, cpu, cpuAdj)
                    print("Move: " + player[37])
                    print("Description: " + player[38])
                    print("1.) Use Move")
                    print("2.) Go Back")
            if num == 1:
                return moveChoice
            else:
                clearscreen()
                asciiRead(player[0], cpu[0])
                statsDisplay(player, cpu)
                hpDisplay(player, playerAdj, cpu, cpuAdj)
                moveDisplay(player)
def modifier(move, attacker, defender):
    modifier = 1.0

    if move == 1:
        modifier = modifier * typeCalc(attacker[12], defender[8], defender[9])
        modifier = modifier * stabBonus(attacker[12], attacker[8], attacker[9])
    elif move == 2:
        modifier = modifier * typeCalc(attacker[21], defender[8], defender[9])
        modifier = modifier * stabBonus(attacker[21], attacker[8], attacker[9])
    elif move == 3:
        modifier = modifier * typeCalc(attacker[30], defender[8], defender[9])
        modifier = modifier * stabBonus(attacker[30], attacker[8], attacker[9])
    elif move == 4:
        modifier = modifier * typeCalc(attacker[39], defender[8], defender[9])
        modifier = modifier * stabBonus(attacker[39], attacker[8], attacker[9])
    return modifier

def randomizedDamage():
    return random.randint(85,100) / 100

def fullDamageCalc(attacker, defender, move):
    damage = AtkBaseDamage(attacker, defender, move) * modifier(move, attacker, defender) * randomizedDamage()
    return damage
def main():
    curses.wrapper(greeter)
    clearscreen()
    
    print("Choose a pokemon to battle with")
    print("1. Venusaur")
    choice = int(input())

 

    party_Pokemon_One = StatDB(choice)
    party_Pkemon_One_Adj = party_Pokemon_One
    CPU_Pokemon_One = CPUChoice()
    CPU_Pokemon_One_Adj = CPU_Pokemon_One
    asciiRead(party_Pokemon_One[0],CPU_Pokemon_One[0])
    statsDisplay(party_Pokemon_One, CPU_Pokemon_One)
    hpDisplay(party_Pokemon_One, party_Pkemon_One_Adj, CPU_Pokemon_One, CPU_Pokemon_One_Adj)
    moveDisplay(party_Pkemon_One_Adj)
    moveChoice = moveChoose(party_Pokemon_One, party_Pkemon_One_Adj, CPU_Pokemon_One, CPU_Pokemon_One_Adj)
    damage = int(fullDamageCalc(party_Pkemon_One_Adj, CPU_Pokemon_One_Adj, moveChoice))
    print(damage)

if __name__ == '__main__':
    main()