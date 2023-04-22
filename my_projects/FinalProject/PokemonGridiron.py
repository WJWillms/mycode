#!/usr/bin/env python3
import numpy as np
import random
import os
import time
import curses
import textwrap
import copy

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

#Poison Calc: damage = floor((maxHP * turn) / 16)

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

#Ascii's courtesy of https://www.fiikus.net/?pokedex
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
            return baseDamage
        elif attacker[13] == 2:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[14] * attacker[4] / defender[6]) /50 + 2)
            return baseDamage
        else:
            print("Run non damaging attack")
    if move == 2:
        if attacker[22] == 1:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[23] * attacker[3] / defender[5]) /50 + 2)
            return baseDamage
        elif attacker[22] == 2:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[23] * attacker[4] / defender[6]) /50 + 2)
            return baseDamage
        else:
            print("Run non damaging attack")
    if move == 3:
        if attacker[31] == 1:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[32] * attacker[3] / defender[5]) /50 + 2)
            return baseDamage
        elif attacker[31] == 2:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[32] * attacker[4] / defender[6]) /50 + 2)
            return baseDamage
        else:
            print("Run non damaging attack")
    if move == 4:
        if attacker[40] == 1:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[41] * attacker[3] / defender[5]) /50 + 2)
            return baseDamage
        elif attacker[40] == 2:
            baseDamage = (((2 * 100 / 5 + 2) * attacker[41] * attacker[4] / defender[6]) /50 + 2)
            return baseDamage
        else:
            print("Run non damaging attack")
    

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
    
    for i in range(player[46]-len(player[1])):
          print(" ", end="")
    print(player[1], end="")      
    print("|                  |", end="")
    print(cpu[1])

def hpDisplay(player, playerAdj, cpu, cpuAdj):
    for i in range(player[46]-len(str(player[2])) - len(str(playerAdj[2])) - 1):
          print(" ", end="")
    print(str(playerAdj[2]) + "/" + str(player[2]) + "|                  |" + str(cpuAdj[2]) + "/" + str(cpu[2]))

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

def fullDamageCalc(attacker, defender, move, attackerOrig, DefenderOrig):
    damage = AtkBaseDamage(attacker, defender, move) * modifier(move, attacker, defender) * randomizedDamage()
    return damage


def userSpecialAbilities(move, userPokemon, effect):
    global userFieldBinaries
    global cpuFieldBinaries
    global weatherBinaries
    global userPokemonOneBinaries
    global cpuPokemonOneBinaries

    global userPokemonOne
    global cpuPokemonOne
    global userPokemonOneAdj
    global cpuPokemonOneAdj
    afterEffect = effect

    #0 No effect
    #1 Leech Seed
    #2 Sludge Bomb or 30% poison chance
    #3 Synthesis
    #4 Hidden Power damage modifier

    if move == 1:
        if userPokemon[18] == 0:
            return
        elif userPokemon[18] == 1:
            if afterEffect == True:
                return
            else:
                if cpuPokemonOneBinaries[7] == False:
                    cpuPokemonOneBinaries[0] = True
                    cpuPokemonOneBinaries[7] = True
                    print("The opposing " + cpuPokemonOne[1] + " was seeded.")
                else:
                    print("The opposing " + cpuPokemonOne[1] + " was already seeded.")
        elif userPokemon[18] == 2:
            if afterEffect == True:
                return
            else:
                num = random.randint(1,100)
                if num > 69:
                    if cpuPokemonOneBinaries[2] == False:
                        print("The opposing " + cpuPokemonOne[1] + " was poisoned.")
                        cpuPokemonOneBinaries[2] = True
                    
        elif userPokemon[18] == 3:
            if afterEffect == True:
                return
            else:
                if weatherBinaries[1] == True:
                    userPokemonOneAdj[2] = userPokemonOneAdj[2] + (userPokemonOne[2] * (2/3))
                elif weatherBinaries[2] == True:
                    userPokemonOneAdj[2] = userPokemonOneAdj[2] + (userPokemonOne[2] * (1/4))
                else:
                    userPokemonOneAdj[2] = userPokemonOneAdj[2] + (userPokemonOne[2] * (1/2))
                print("Your " + userPokemon[1] + " was healed.")
                if userPokemonOneAdj[2] > userPokemonOne[2]:
                    userPokemonOneAdj[2] = userPokemonOne[2]
        elif userPokemon[18] == 4:
            num = random.randint(30,70)
            userPokemonOneAdj[14] = num




    elif move == 2:
        if userPokemon[27] == 0:
            return
        elif userPokemon[27] == 1:
            if afterEffect == True:
                return
            else:
                if cpuPokemonOneBinaries[7] == False:
                    cpuPokemonOneBinaries[0] = True
                    cpuPokemonOneBinaries[7] = True
                    print("The opposing " + cpuPokemonOne[1] + " was seeded.")
                else:
                    print("The opposing " + cpuPokemonOne[1] + " was already seeded.")
        elif userPokemon[27] == 2:
            if afterEffect == True:
                return
            else:
                num = random.randint(1,100)
                if num > 69:
                    if cpuPokemonOneBinaries[2] == False:
                        print("The opposing " + cpuPokemonOne[1] + " was poisoned.")
                        cpuPokemonOneBinaries[2] = True
        elif userPokemon[27] == 3:
            if afterEffect == True:
                return
            else:
                if weatherBinaries[1] == True:
                    userPokemonOneAdj[2] = userPokemonOneAdj[2] + (userPokemonOne[2] * (2/3))
                elif weatherBinaries[2] == True:
                    userPokemonOneAdj[2] = userPokemonOneAdj[2] + (userPokemonOne[2] * (1/4))
                else:
                    userPokemonOneAdj[2] = userPokemonOneAdj[2] + (userPokemonOne[2] * (1/2))
                print("Your " + userPokemon[1] + " was healed.")
                if userPokemonOneAdj[2] > userPokemonOne[2]:
                    userPokemonOneAdj[2] = userPokemonOne[2]
        elif userPokemon[27] == 4:
            num = random.randint(30,70)
            userPokemonOneAdj[23] = num



    elif move == 3:
        if userPokemon[36] == 0:
            return
        elif userPokemon[36] == 1:
            if afterEffect == True:
                return
            else:
                if cpuPokemonOneBinaries[7] == False:
                    cpuPokemonOneBinaries[0] = True
                    cpuPokemonOneBinaries[7] = True
                    print("The opposing " + cpuPokemonOne[1] + " was seeded.")
                else:
                    print("The opposing " + cpuPokemonOne[1] + " was already seeded.")
        elif userPokemon[36] == 2:
            if afterEffect == True:
                return
            else:
                num = random.randint(1,100)
                if num > 69:
                    if cpuPokemonOneBinaries[2] == False:
                        print("The opposing " + cpuPokemonOne[1] + " was poisoned.")
                        cpuPokemonOneBinaries[2] = True
        elif userPokemon[36] == 3:
            if afterEffect == True:
                return
            else:
                if weatherBinaries[1] == True:
                    userPokemonOneAdj[2] = userPokemonOneAdj[2] + (userPokemonOne[2] * (2/3))
                elif weatherBinaries[2] == True:
                    userPokemonOneAdj[2] = userPokemonOneAdj[2] + (userPokemonOne[2] * (1/4))
                else:
                    userPokemonOneAdj[2] = userPokemonOneAdj[2] + (userPokemonOne[2] * (1/2))
                print("Your " + userPokemon[1] + " was healed.")
                if userPokemonOneAdj[2] > userPokemonOne[2]:
                    userPokemonOneAdj[2] = userPokemonOne[2]
        elif userPokemon[36] == 4:
            num = random.randint(30,70)
            userPokemonOneAdj[32] = num




    elif move == 4:
        if userPokemon[45] == 0:
            return
        elif userPokemon[45] == 1:
            if afterEffect == True:
                return
            else:
                if cpuPokemonOneBinaries[7] == False:
                    cpuPokemonOneBinaries[0] = True
                    cpuPokemonOneBinaries[7] = True
                    print("The opposing " + cpuPokemonOne[1] + " was seeded.")
                else:
                    print("The opposing " + cpuPokemonOne[1] + " was already seeded.")
        elif userPokemon[45] == 2:
            if afterEffect == True:
                return
            else:
                num = random.randint(1,100)
                if num > 69:
                    if cpuPokemonOneBinaries[2] == False:
                        print("The opposing " + cpuPokemonOne[1] + " was poisoned.")
                        cpuPokemonOneBinaries[2] = True
        elif userPokemon[45] == 3:
            if afterEffect == True:
                return
            else:
                if weatherBinaries[1] == True:
                    userPokemonOneAdj[2] = userPokemonOneAdj[2] + (userPokemonOne[2] * (2/3))
                elif weatherBinaries[2] == True:
                    userPokemonOneAdj[2] = userPokemonOneAdj[2] + (userPokemonOne[2] * (1/4))
                else:
                    userPokemonOneAdj[2] = userPokemonOneAdj[2] + (userPokemonOne[2] * (1/2))
                print("Your " + userPokemon[1] + " was healed.")
                if userPokemonOneAdj[2] > userPokemonOne[2]:
                    userPokemonOneAdj[2] = userPokemonOne[2]
        elif userPokemon[45] == 4:
            num = random.randint(30,70)
            userPokemonOneAdj[41] = num




def cpuSpecialAbilities(move, cpuPokemon, effect):
    global userFieldBinaries
    global cpuFieldBinaries
    global weatherBinaries
    global userPokemonOneBinaries
    global cpuPokemonOneBinaries

    global userPokemonOne
    global cpuPokemonOne
    global userPokemonOneAdj
    global cpuPokemonOneAdj
    afterEffect = effect

    #0 No effect
    #1 Leech Seed
    #2 Sludge Bomb or 30% poison chance
    #3 Synthesis
    #4 Hidden Power damage modifier

    if move == 1:
        if cpuPokemon[18] == 0:
            return
        elif cpuPokemon[18] == 1:
            if afterEffect == True:
                return
            else:
                if userPokemonOneBinaries[7] == False:
                    userPokemonOneBinaries[0] = True
                    userPokemonOneBinaries[7] = True
                    print("your " + userPokemonOne[1] + " was seeded.")
                else:
                    print("your " + userPokemonOne[1] + " was already seeded.")
        elif cpuPokemon[18] == 2:
            if afterEffect == True:
                return
            else:
                num = random.randint(1,100)
                if num > 69:
                    if userPokemonOneBinaries[2] == False:
                        print("The opposing " + userPokemonOne[1] + " was poisoned.")
                        userPokemonOneBinaries[2] = True
                    
        elif cpuPokemon[18] == 3:
            if afterEffect == True:
                return
            else:
                if weatherBinaries[1] == True:
                    cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] + (cpuPokemonOne[2] * (2/3))
                elif weatherBinaries[2] == True:
                    cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] + (cpuPokemonOne[2] * (1/4))
                else:
                    cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] + (cpuPokemonOne[2] * (1/2))
                print("The opposing " + cpuPokemon[1] + " was healed.")
                if cpuPokemonOneAdj[2] > cpuPokemonOne[2]:
                    cpuPokemonOneAdj[2] = cpuPokemonOne[2]
        elif cpuPokemon[18] == 4:
            num = random.randint(30,70)
            cpuPokemonOneAdj[14] = num


    elif move == 2:
        if cpuPokemon[27] == 0:
            return
        elif cpuPokemon[27] == 1:
            if afterEffect == True:
                return
            else:
                if userPokemonOneBinaries[7] == False:
                    userPokemonOneBinaries[0] = True
                    userPokemonOneBinaries[7] = True
                    print("Your " + userPokemonOne[1] + " was seeded.")
                else:
                    print("Your " + userPokemonOne[1] + " was already seeded.")
        elif cpuPokemon[27] == 2:
            if afterEffect == True:
                return
            else:
                num = random.randint(1,100)
                if num > 69:
                    if userPokemonOneBinaries[2] == False:
                        print("Your " + userPokemonOne[1] + " was poisoned.")
                        userPokemonOneBinaries[2] = True
        elif cpuPokemon[27] == 3:
            if afterEffect == True:
                return
            else:
                if weatherBinaries[1] == True:
                    cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] + (cpuPokemonOne[2] * (2/3))
                elif weatherBinaries[2] == True:
                    cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] + (cpuPokemonOne[2] * (1/4))
                else:
                    cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] + (cpuPokemonOne[2] * (1/2))
                print("The opposing " + cpuPokemon[1] + " was healed.")
                if cpuPokemonOneAdj[2] > cpuPokemonOne[2]:
                    cpuPokemonOneAdj[2] = cpuPokemonOne[2]
        elif cpuPokemon[27] == 4:
            num = random.randint(30,70)
            cpuPokemonOneAdj[23] = num


    elif move == 3:
        if cpuPokemon[36] == 0:
            return
        elif cpuPokemon[36] == 1:
            if afterEffect == True:
                return
            else:
                if userPokemonOneBinaries[7] == False:
                    userPokemonOneBinaries[0] = True
                    userPokemonOneBinaries[7] = True
                    print("Your " + userPokemonOne[1] + " was seeded.")
                else:
                    print("Your " + userPokemonOne[1] + " was already seeded.")
        elif cpuPokemon[36] == 2:
            if afterEffect == True:
                return
            else:
                num = random.randint(1,100)
                if num > 69:
                    if userPokemonOneBinaries[2] == False:
                        print("Your " + userPokemonOne[1] + " was poisoned.")
                        userPokemonOneBinaries[2] = True
        elif cpuPokemon[36] == 3:
            if afterEffect == True:
                return
            else:
                if weatherBinaries[1] == True:
                    cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] + (cpuPokemonOne[2] * (2/3))
                elif weatherBinaries[2] == True:
                    cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] + (cpuPokemonOne[2] * (1/4))
                else:
                    cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] + (cpuPokemonOne[2] * (1/2))
                print("The opposing " + cpuPokemon[1] + " was healed.")
                if cpuPokemonOneAdj[2] > cpuPokemonOne[2]:
                    cpuPokemonOneAdj[2] = cpuPokemonOne[2]
        elif cpuPokemon[36] == 4:
            num = random.randint(30,70)
            cpuPokemonOneAdj[32] = num


    elif move == 4:
        if cpuPokemon[45] == 0:
            return
        elif cpuPokemon[45] == 1:
            if afterEffect == True:
                return
            else:
                if userPokemonOneBinaries[7] == False:
                    userPokemonOneBinaries[0] = True
                    userPokemonOneBinaries[7] = True
                    print("Your " + userPokemonOne[1] + " was seeded.")
                else:
                    print("Your " + userPokemonOne[1] + " was already seeded.")
        elif cpuPokemon[45] == 2:
            if afterEffect == True:
                return
            else:
                num = random.randint(1,100)
                if num > 69:
                    if userPokemonOneBinaries[2] == False:
                        print("Your " + userPokemonOne[1] + " was poisoned.")
                        userPokemonOneBinaries[2] = True
        elif cpuPokemon[45] == 3:
            if afterEffect == True:
                return
            else:
                if weatherBinaries[1] == True:
                    cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] + (cpuPokemonOne[2] * (2/3))
                elif weatherBinaries[2] == True:
                    cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] + (cpuPokemonOne[2] * (1/4))
                else:
                    cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] + (cpuPokemonOne[2] * (1/2))
                print("The opposing " + cpuPokemon[1] + " was healed.")
                if cpuPokemonOneAdj[2] > cpuPokemonOne[2]:
                    cpuPokemonOneAdj[2] = cpuPokemonOne[2]
        elif cpuPokemon[45] == 4:
            num = random.randint(30,70)
            cpuPokemonOneAdj[41] = num


def speedCalc(user, userAdj, cpu, cpuAdj):
    if userAdj > cpuAdj:
        return 1
    elif cpuAdj > userAdj:
        return 2
    elif cpuAdj == userAdj:
        return random.randint(1, 2)

def accuracyCalc(attacker, attackerAdj, defender, defenderAdj, move):
    hit = False
    if move == 1:
        num = random.randint(1,100)
        if num > attackerAdj[15]:
            hit = False
        else:
            hit = True
    elif move == 2:
        num = random.randint(1,100)
        if num > attackerAdj[24]:
            hit = False
        else:
            hit = True
    elif move == 3:
        num = random.randint(1,100)
        if num > attackerAdj[33]:
            hit = False
        else:
            hit = True
    elif move == 4:
        num = random.randint(1,100)
        if num > attackerAdj[42]:
            hit = False
        else:
            hit = True
    return hit

def moveEffectivenessPrint(attacker, defender, move):
    if move == 1:
        effectiveOut = typeCalc(attacker[12], defender[8], defender[9])
        if effectiveOut > 1:
            print("It was super effective")
        elif effectiveOut < 1:
            print("It wasn't very effective")
        else:
            print(attacker[10] + " hit the opposing " + defender[1])
    elif move == 2:
        effectiveOut = typeCalc(attacker[21], defender[8], defender[9])
        if effectiveOut > 1:
            print("It was super effective")
        elif effectiveOut < 1:
            print("It wasn't very effective")
        else:
            print(attacker[19] + " hit the opposing " + defender[1])
    elif move == 3:
        effectiveOut = typeCalc(attacker[30], defender[8], defender[9])
        if effectiveOut > 1:
            print("It was super effective")
        elif effectiveOut < 1:
            print("It wasn't very effective")
        else:
            print(attacker[28] + " hit the opposing " + defender[1])
    elif move == 4:
        effectiveOut = typeCalc(attacker[39], defender[8], defender[9])
        if effectiveOut > 1:
            print("It was super effective")
        elif effectiveOut < 1:
            print("It wasn't very effective")
        else:
            print(attacker[37] + " hit the opposing " + defender[1])
    
    
def cpuMoveChooser():
    return random.randint(1,4)


def main():
    curses.wrapper(greeter)
    clearscreen()


    #Making everything global because I hate my life
    global userFieldBinaries
    global cpuFieldBinaries
    global weatherBinaries
    global binariesTemplate
    global userPokemonOneBinaries
    global cpuPokemonOneBinaries
    global userPokemonOne
    global userPokemonOneAdj
    global cpuPokemonOne
    global cpuPokemonOneAdj




    #FieldCondition, Spikes, Toxic Spikes, Stealth Rocks
    userFieldBinaries = [False, False, False, False]
    cpuFieldBinaries = [False, False, False, False]
    #Weather Condition, Sunny, Raining
    weatherBinaries = [False, False, False]
    #Status Condition, Burn, Poison, Paralyze, Freeze, Sleep, Confusion, Leech Seeded
    binariesTemplate = [False, False, False, False, False, False ,False, False]
    userPokemonOneBinaries = binariesTemplate
    cpuPokemonOneBinaries = binariesTemplate



    while True:
        print("Choose a pokemon to battle with")
        print("1. Venusaur")
        choice = input("Choice: ")
        if choice.isdigit() and int(choice) in range(1, 2):
            choice = int(choice)
            break
        else:
            print("Invalid Choice")
            time.sleep(1.4)
            clearscreen()
    clearscreen()
    userPokemonOne = StatDB(choice)
    userPokemonOneAdj = copy.deepcopy(userPokemonOne)
    cpuPokemonOne = CPUChoice()
    cpuPokemonOneAdj = copy.deepcopy(cpuPokemonOne)


    while userPokemonOneAdj[2] > 0 and cpuPokemonOneAdj[2] > 0:
        asciiRead(userPokemonOne[0],cpuPokemonOne[0])
        statsDisplay(userPokemonOne, cpuPokemonOne)
        hpDisplay(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj)
        moveDisplay(userPokemonOneAdj)
        moveChoice = moveChoose(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj)
        cpuMove = cpuMoveChooser()
        fastest = speedCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj)
        #Fastest 1 = User, 2 = Cpu
        if fastest == 1:
            #User Attack
            if moveChoice == 1:
                if userPokemonOneAdj[13] == 1 or userPokemonOneAdj[13] == 2:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[10] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice, userPokemonOne, cpuPokemonOne))
                        cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
                    else:
                        print(userPokemonOne[10] + " missed " + cpuPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[10] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
            elif moveChoice == 2:
                if userPokemonOneAdj[22] == 1 or userPokemonOneAdj[22] == 2:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[19] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice, userPokemonOne, cpuPokemonOne))
                        cpuPokemonOneAdj[2] -=damage
                        moveEffectivenessPrint(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice)
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
                    else:
                        print(userPokemonOne[19] + " missed " + cpuPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[19] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
            elif moveChoice == 3:
                if userPokemonOneAdj[31] == 1 or userPokemonOneAdj[31] == 2:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[28] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice, userPokemonOne, cpuPokemonOne))
                        cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice)
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
                    else:
                        print(userPokemonOne[28] + " missed " + cpuPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[28] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
            elif moveChoice == 4:
                if userPokemonOneAdj[40] == 1 or userPokemonOneAdj[40] == 2:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[37] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice, userPokemonOne, cpuPokemonOne))
                        cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice)
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
                    else:
                        print(userPokemonOne[37] + " missed " + cpuPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[37] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)


            #CPU Attack
            if cpuMove == 1:
                if cpuPokemonOneAdj[13] == 1 or cpuPokemonOneAdj[13] == 2:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[10] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove, cpuPokemonOne, userPokemonOne))
                        userPokemonOneAdj[2] = userPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
                    else:
                        print(cpuPokemonOne[10] + " missed your " + userPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[10] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
            elif cpuMove == 2:
                if cpuPokemonOneAdj[22] == 1 or cpuPokemonOneAdj[22] == 2:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[19] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove, cpuPokemonOne, userPokemonOne))
                        userPokemonOneAdj[2] = userPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
                    else:
                        print(cpuPokemonOne[19] + " missed your " + userPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[19] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
            elif cpuMove == 3:
                if cpuPokemonOneAdj[31] == 1 or cpuPokemonOneAdj[31] == 2:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[28] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove, cpuPokemonOne, userPokemonOne))
                        userPokemonOneAdj[2] = userPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
                    else:
                        print(cpuPokemonOne[28] + " missed your " + userPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[28] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
            elif cpuMove == 4:
                if cpuPokemonOneAdj[40] == 1 or cpuPokemonOneAdj[40] == 2:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[37] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove, cpuPokemonOne, userPokemonOne))
                        userPokemonOneAdj[2] = userPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
                    else:
                        print(cpuPokemonOne[37] + " missed your " + userPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[37] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
        else:
            #CPU Attack
            if cpuMove == 1:
                if cpuPokemonOneAdj[13] == 1 or cpuPokemonOneAdj[13] == 2:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[10] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove, cpuPokemonOne, userPokemonOne))
                        userPokemonOneAdj[2] = userPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
                    else:
                        print(cpuPokemonOne[10] + " missed your " + userPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[10] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
            elif cpuMove == 2:
                if cpuPokemonOneAdj[22] == 1 or cpuPokemonOneAdj[22] == 2:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[19] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove, cpuPokemonOne, userPokemonOne))
                        userPokemonOneAdj[2] = userPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
                    else:
                        print(cpuPokemonOne[19] + " missed your " + userPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[19] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
            elif cpuMove == 3:
                if cpuPokemonOneAdj[31] == 1 or cpuPokemonOneAdj[31] == 2:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[28] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove, cpuPokemonOne, userPokemonOne))
                        userPokemonOneAdj[2] = userPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
                    else:
                        print(cpuPokemonOne[28] + " missed your " + userPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[28] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
            elif cpuMove == 4:
                if cpuPokemonOneAdj[40] == 1 or cpuPokemonOneAdj[40] == 2:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[37] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove, cpuPokemonOne, userPokemonOne))
                        userPokemonOneAdj[2] = userPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(cpuPokemonOneAdj, userPokemonOneAdj, cpuMove)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
                    else:
                        print(cpuPokemonOne[37] + " missed your " + userPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, True)
                    print(cpuPokemonOneAdj[1] + " used " + cpuPokemonOneAdj[37] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(cpuPokemonOne, cpuPokemonOneAdj, userPokemonOne, userPokemonOneAdj, cpuMove)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        cpuSpecialAbilities(cpuMove, cpuPokemonOneAdj, False)
            #User Attack
            if moveChoice == 1:
                if userPokemonOneAdj[13] == 1 or userPokemonOneAdj[13] == 2:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[10] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice, userPokemonOne, cpuPokemonOne))
                        cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
                    else:
                        print(userPokemonOne[10] + " missed " + cpuPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[10] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
            elif moveChoice == 2:
                if userPokemonOneAdj[22] == 1 or userPokemonOneAdj[22] == 2:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[19] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice, userPokemonOne, cpuPokemonOne))
                        cpuPokemonOneAdj[2] -=damage
                        moveEffectivenessPrint(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice)
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
                    else:
                        print(userPokemonOne[19] + " missed " + cpuPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[19] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
            elif moveChoice == 3:
                if userPokemonOneAdj[31] == 1 or userPokemonOneAdj[31] == 2:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[28] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice, userPokemonOne, cpuPokemonOne))
                        cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice)
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
                    else:
                        print(userPokemonOne[28] + " missed " + cpuPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[28] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
            elif moveChoice == 4:
                if userPokemonOneAdj[40] == 1 or userPokemonOneAdj[40] == 2:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[37] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        damage = int(fullDamageCalc(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice, userPokemonOne, cpuPokemonOne))
                        cpuPokemonOneAdj[2] = cpuPokemonOneAdj[2] - damage
                        moveEffectivenessPrint(userPokemonOneAdj, cpuPokemonOneAdj, moveChoice)
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False)
                    else:
                        print(userPokemonOne[37] + " missed " + cpuPokemonOne[1] +".")
                        time.sleep(.7)
                else:
                    userSpecialAbilities(moveChoice, userPokemonOneAdj, True)
                    print(userPokemonOneAdj[1] + " used " + userPokemonOneAdj[37] + ".")
                    time.sleep(.7)
                    moveAccuracy = accuracyCalc(userPokemonOne, userPokemonOneAdj, cpuPokemonOne, cpuPokemonOneAdj, moveChoice)
                    if moveAccuracy == True:
                        time.sleep(.7)
                        userSpecialAbilities(moveChoice, userPokemonOneAdj, False) 
if __name__ == '__main__':
    main()