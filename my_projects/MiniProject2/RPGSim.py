#!/usr/bin/python3
"""Driving a simple game framework with
   a dictionary object | Alta3 Research"""

def showInstructions():
    """Show the game instructions when called"""
    #print a main menu and the commands
    print('''
    RPG Game
    ========
    Commands:
      go [direction]
      get [item]
    ''')

def showStatus(rooms, currentRoom, inventory):
    """determine the current status of the player"""
    # print the player's current location
    print('---------------------------')
    print('You are in the ' + currentRoom)
    # print what the player is carrying
    print('Inventory:', inventory)
    # check if there's an item in the room, if so print it
    if "item" in rooms[currentRoom]:
      print('You see a ' + rooms[currentRoom]['item'])
    print("---------------------------")


def main():
    # an inventory, which is initially empty
    inventory = []

# a dictionary linking a room to other rooms
    rooms = {

            'Room1' : {
                  'north' : 'Room2',
                  'east'  : 'Room4',
                  'south' : 'Room6',
                  'west'  : 'Room8'
                  
                },

            'Room2' : {
                  'north' : 'Room10',
                  'east'  : 'Room3',
                  'south' : 'Room1',
                  'west'  : 'Room9',
                  'item'  : 'Monster'
                  
                },
            'Room3' : {
                  'north' : 'Room11',
                  'east'  : 'Room13',
                  'south' : 'Room4',
                  'west'  : 'Room2'
                  
                },
            'Room4' : {
                  'north' : 'Room3',
                  'east'  : 'Room14',
                  'south' : 'Room5',
                  'west'  : 'Room1'
                  
                },
            'Room5' : {
                  'north' : 'Room4',
                  'east'  : 'Room15',
                  'south' : 'Room17',
                  'west'  : 'Room6',
                  'item'  : 'Monster'
                  },
            'Room6' : {
                  'north' : 'Room1',
                  'east'  : 'Room5',
                  'south' : 'Room18',
                  'west'  : 'Room7'
                  },
            'Room7' : {
                  'north' : 'Room8',
                  'east'  : 'Room6',
                  'south' : 'Room19',
                  'west'  : 'Room21'
                  },
            'Room8' : {
                  'north' : 'Room9',
                  'east'  : 'Room1',
                  'south' : 'Room7',
                  'west'  : 'Room22'
                  },
            'Room9' : {
                  'north' : 'Room25',
                  'east'  : 'Room2',
                  'south' : 'Room8',
                  'west'  : 'Room23'
                  },
            'Room10' : {
                  'east'  : 'Room11',
                  'south' : 'Room2',
                  'west'  : 'Room25'
                  },
            'Room11' : {
                  'east'  : 'Room12',
                  'south' : 'Room3',
                  'west'  : 'Room10',
                  'item'  : 'Monster'
                  },
            'Room12' : {
                  'south' : 'Room13',
                  'west'  : 'Room11'
                  },
            'Room13' : {
                  'north' : 'Room12',
                  'south' : 'Room14',
                  'west'  : 'Room3'
                  },
            'Room14' : {
                  'north' : 'Room13',
                  'south' : 'Room15',
                  'west'  : 'Room4',
                  'item'  : 'Monster'
                  },
            'Room15' : {
                  'north' : 'Room14',
                  'south' : 'Room16',
                  'west'  : 'Room5',
                  'item'  : 'key2'
                  },
            'Room16' : {
                  'north' : 'Room15',
                  'west'  : 'Room17'
                  },
            'Room17' : {
                  'north' : 'Room5',
                  'east'  : 'Room16',
                  'west'  : 'Room18'
                  },
            'Room18' : {
                  'north' : 'Room6',
                  'east'  : 'Room17',
                  'west'  : 'Room19'
                  },
            'Room19' : {
                  'north' : 'Room7',
                  'east'  : 'Room18',
                  'west'  : 'Room20'
                  },
            'Room20' : {
                  'north' : 'Room21',
                  'east'  : 'Room19',
                  },
            'Room21' : {
                  'north' : 'Room22',
                  'east'  : 'Room7',
                  'south' : 'Room20',
                  'item'  : 'Monster'
                  },
            'Room22' : {
                  'north' : 'Room23',
                  'east'  : 'Room8',
                  'south' : 'Room21',
                  },
            'Room23' : {
                  'north' : 'Room24',
                  'east'  : 'Room9',
                  'south' : 'Room22',
                  'item'  : 'key1'
                  },
            'Room24' : {
                  'east'  : 'Room25',
                  'south' : 'Room23',
                  },
            'Room25' : {
                  'east'  : 'Room10',
                  'south' : 'Room9',
                  'west'  : 'Room24'
                  },
         }

# start the player in Room1
    currentRoom = 'Room1'
    showInstructions()

# breaking this while loop means the game is over
    while True:
        showStatus(rooms, currentRoom, inventory)

        # the player MUST type something in
        # otherwise input will keep asking
        move = ''
        while move == '':  
            move = input('>')

        # normalizing input:
        # .lower() makes it lower case, .split() turns it to a list
        # therefore, "get golden key" becomes ["get", "golden key"]          
        move = move.lower().split(" ", 1)

        #if they type 'go' first
        if move[0] == 'go':
            #check that they are allowed wherever they want to go
            if move[1] in rooms[currentRoom]:
                #set the current room to the new room
                currentRoom = rooms[currentRoom][move[1]]
            # if they aren't allowed to go that way:
            else:
                print('You can\'t go that way!')

        #if they type 'get' first
        if move[0] == 'get' :
            # make two checks:
            # 1. if the current room contains an item
            # 2. if the item in the room matches the item the player wishes to get
            if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
                #add the item to their inventory
                inventory.append(move[1])
                #display a helpful message
                print(move[1] + ' got!')
                #delete the item key:value pair from the room's dictionary
                del rooms[currentRoom]['item']
            # if there's no item in the room or the item doesn't match
            else:
                print(currentRoom)
                print(move[1])
                print(rooms[currentRoom]['item'])
                #tell them they can't get it
                print('Can\'t get ' + move[1] + '!')
        if 'item' in rooms[currentRoom] and 'Monster' in rooms[currentRoom]['item']:
            print('A monster has got you... GAME OVER!')
            break
        if 'key1' in inventory and 'key2' in inventory:
            print('You found both the keys needed to escape... YOU WIN!')
            break

if __name__ == "__main__":
    main()