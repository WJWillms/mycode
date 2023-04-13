#!/usr/bin/python3
#Fail Counter
loginfail = 0
#Open File
keystone_file = open("/home/student/mycode/attemptlogin/keystone.common.wsgi","r")
#Make a list of all lines in the file
keystone_file_lines=keystone_file.readlines()
#Loop through list looking for fail and incrementing the count when condition is met
for line in keystone_file_lines:
	if "- - - - -] Authorization failed" in line:
		loginfail += 1
print("The number of failed log in attempts is", loginfail)
#Close File
keystone_file.close()
