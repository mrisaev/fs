import win32net
import win32security
import sys
import os
import xml.etree.ElementTree as ET


tserver = sys.argv[1]
audit = []

shareresume=0
sharelist = []
while 1:
    sharedata, total, shareresume = win32net.NetShareEnum(tserver, 2, shareresume)
    for share in sharedata:
        if "$" not in share['netname']:
            sharelist.append(share['netname'])
            print 'Share name - ', share['netname']
    if not shareresume:
        break

def getsddl(path):
    fname = path
    sd = win32security.GetFileSecurity(fname, win32security.DACL_SECURITY_INFORMATION)
    sddl = win32security.ConvertSecurityDescriptorToStringSecurityDescriptor(sd, win32security.SDDL_REVISION_1, win32security.DACL_SECURITY_INFORMATION)
    print path
    print str(sddl)
    return sddl


def revealDACL(wara):
    rootdir = '\\\\' + str(tserver) + '\\' + wara
    sddl = getsddl(rootdir)

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            tgt = os.path.join(subdir, file)
            sddl = getsddl(tgt)

    for subdir, dirs, files in os.walk(rootdir):
        for dir in dirs:
            tgt = os.path.join(subdir, dir)
            sddl = getsddl(tgt)

for wara in sharelist:
    revealDACL(wara)