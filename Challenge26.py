#!/usr/bin/env python3
def main():
    
    cont = ""
    while cont != "1":
    
    
    
        char_name=""
        while char_name != "Starlord" and char_name != "Mystique" and char_name != "Hulk":
            char_name = input("Which character do you want to know about? (Starlord, Mystique, Hulk)")
            char_name = char_name.capitalize()
        
    
        char_stat=""
        while char_stat != "real name" and char_stat != "powers" and char_stat != "archenemy":
            char_stat = input(" What statistic do you want to know about? (real name, powers, archenemy)")
            char_stat = char_stat.lower()
      
        marvelchars= {
        "Starlord":
        {"real name": "peter quill",
        "powers": "dance moves",
        "archenemy": "Thanos"},

        "Mystique":
        {"real name": "raven darkholme",
        "powers": "shape shifter",
        "archenemy": "Professor X"},

        "Hulk":
        {"real name": "bruce banner",
        "powers": "super strength",
        "archenemy": "adrenaline"}
        }

        if char_stat == "real name":
            print(char_name + "'s " + char_stat + " is: " + marvelchars[char_name][char_stat].title())
        else:
            print(char_name + "'s " + char_stat + " is: " + marvelchars[char_name][char_stat])
        
        cont = input("Enter any button to try again or 1 to quit: ")





if __name__ == '__main__':
    main()