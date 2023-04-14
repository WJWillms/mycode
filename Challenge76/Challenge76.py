#!/usr/bin/env python3

import requests
import json
import pprint

def main():
    pokenum = input("Pick a number between 1 and 151!\n>")
    pokeapi = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokenum).json()

    print("Number " + str(pokenum) + "'s Name: ",pokeapi["name"])
    print("Moves:")
    print("----------------------------")
    for move in pokeapi['moves']:
        print(' >', move['move']['name']) 
    print("Stats: ")   
    print("----------------------------")
    for stat in pokeapi['stats']:
        print(' >', stat['stat']['name'] , stat['base_stat']) 
if __name__ == "__main__":
    main()