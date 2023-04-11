#!/usr/bin/python

wordbank= ["indentation", "spaces"] 

tlgstudents= ['Albert', 'Anthony', 'Brenden', 'Craig', 'Deja', 'Elihu', 'Eric', 'Giovanni', 'James', 'Joshua', 'Maria', 'Mohamed', 'PJ', 'Philip', 'Sagan', 'Suchit', 'Meka', 'Trey', 'Winton', 'Xiuxiang', 'Yaping']

wordbank.append(4)


num=-1
while num < 0 or num > len(tlgstudents):
        num = int(input("Pick a number between 1 and " + str(len(tlgstudents)) +": "))


student_name = tlgstudents[num-1]

print(student_name + " always uses " + str(wordbank[2]) + " " + str(wordbank[1]) + " to indent")
