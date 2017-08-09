# Enumerate shares on server

import win32net
import sys
import subprocess


shareresume = 0
x = sys.argv[1]
while 1:
    sharedata, total, shareresume = win32net.NetShareEnum(x, 2, shareresume)
    for share in sharedata:
        print(" %(netname)s (%(path)s):%(remark)s - in use by %(current_uses)d users type %(type)s" % share)
    if not shareresume:
        break
