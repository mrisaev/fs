# Get share information

import win32net
import win32netcon
import win32security
import sys

server = sys.argv[1]
share = sys.argv[2]
print win32net.NetShareGetInfo(server, share, 502)