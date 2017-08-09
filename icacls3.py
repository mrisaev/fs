# Create 1000 users and set on given file system object 2 discretionary
# ACE for each

import subprocess
import sys

obj = sys.argv[0]
x = 1
y = 1000
f = open('scr.bat', 'w')
while x < 2000:
    y = y + 1
    f.write('net user /add ' + str(y) + '\n')
    f.write('icacls' + obj + '/grant ' + str(y) + ':(F) \n')
    f.write('icacls' + obj + '/deny ' + str(y) + ':(R) \n')
	#f.write('icacls' + obj + '/remove ' + str(y) + ' \n' )
	x = x + 1
f.close()

subprocess.Popen('scr.bat', shell=True)


# Remove 1000 users
'''
x = 1
y = 1000
f = open('delete_users.bat', 'w')
while x<2000:
	y=y+1
	f.write('net user /delete ' + str(y) + '\n' ) 
        x=x+1
f.close()

'''
