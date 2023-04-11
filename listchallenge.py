#!/usr/bin/python

heroes= ["Spiderman", "Batman", "Black Panther", "Wonder Woman", "Storm"]

# PART 1
# Print out your favorite character from this list! The output would look something like:
# My favorite character is Black Panther!
print("My favorite character is " + str(heroes[0]) + "!")

# PART 2
# Ask the user to pick a number between 1 and 100.
# Convert the input into an integer.
num=-1
while num < 1 or num > 100:
	num = int(input("Pick a number between 1 and 100: "))

nums= [1, -5, 56, 987, 0]

# PART 3
# check out https://docs.python.org/3/library/functions.html or go to Google
# use a built-in function to find which integer in nums is the biggest.
# then, print out that number!

max_num = max(nums)
print("The biggest number is: " + str(max_num))
