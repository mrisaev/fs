# This script validates SACL SDDLs on all shared files system objects
# Read access requiered

import win32net
import win32security
import sys
import os
import xml.etree.ElementTree as ET

# get audit configuration from configuration.xml using XPath
targetServer = sys.argv[1]
audit = []
nodes = ['.//n[@n="ManagedObjects"].//n[@n="ScopeItems"]//a[@v="' + 
         targetServer + '"]/../../..//a[@n="SuccessfulModificationsEnabled"]',
         './/n[@n="ManagedObjects"].//n[@n="ScopeItems"]//a[@v="' +
         targetServer + '"]/../../..//a[@n="SuccessfulReadsEnabled"]',
         './/n[@n="ManagedObjects"].//n[@n="ScopeItems"]//a[@v="' +
         targetServer + '"]/../../..//a[@n="FailedModificationsEnabled"]',
         './/n[@n="ManagedObjects"].//n[@n="ScopeItems"]//a[@v="' +
         targetServer + '"]/../../..//a[@n="FailedReadsEnabled"]']

aud = ["SuccessfulModificationsEnabled - ", "SuccessfulReadsEnabled - ",
       "FailedModificationsEnabled - ", "FailedReadsEnabled - "]
tree = ET.parse('Configuration.xml')
conf = tree.getroot()
ind = 0
for i in nodes:
    sss = conf.findall(i)
    param = sss[0].get('v')
    audit.append(param)
    print aud[ind], param
    ind = ind + 1

if audit[0] == 'False':
    audit[0] = 'True'
print str(audit) + ' - Resultant config'

# Define etalon SDDL constants
# Modify success
if audit == ['True', 'False', 'False', 'False']:
    value = [
        '(AU;OICISA;DCLCRPDTCRSDWDWO;;;WD)',
        '(AU;OICIIDSA;DCLCRPDTCRSDWDWO;;;WD)',
        '(AU;IDSA;DCLCRPDTCRSDWDWO;;;WD)',
        '(AU;SA;DCLCRPDTCRSDWDWO;;;WD)']

# Modify success Read success
if audit == ['True', 'True', 'False', 'False']:
    value = [
        '(AU;OIIOSA;CC;;;WD)(AU;OICISA;DCLCRPDTCRSDWDWO;;;WD)',
        '(AU;OIIOIDSA;CC;;;WD)(AU;OICIIDSA;DCLCRPDTCRSDWDWO;;;WD)',
        '(AU;IDSA;CC;;;WD)(AU;IDSA;DCLCRPDTCRSDWDWO;;;WD)',
        '(AU;SA;CC;;;WD)(AU;SA;DCLCRPDTCRSDWDWO;;;WD)']

# Modify success Read failed
if audit == ['True', 'False', 'False', 'True']:
    value = [
        '(AU;OICISA;DCLCRPDTCRSDWDWO;;;WD)(AU;OICIFA;CC;;;WD)',
        '(AU;OICIIDSA;DCLCRPDTCRSDWDWO;;;WD)(AU;OICIIDFA;CC;;;WD)',
        '(AU;IDSA;DCLCRPDTCRSDWDWO;;;WD)(AU;IDFA;CC;;;WD)',
        '(AU;SA;DCLCRPDTCRSDWDWO;;;WD)(AU;FA;CC;;;WD)']

# Modify success\failed
if audit == ['True', 'False', 'True', 'False']:
    value = [
        '(AU;OICISA;DCLCRPDTCRSDWDWO;;;WD)(AU;OICIFA;DCLCRPDTCRSDWDWO;;;WD)',
        '(AU;OICIIDSA;DCLCRPDTCRSDWDWO;;;WD)(AU;OICIIDFA;DCLCRPDTCRSDWDWO;;;WD)',
        '(AU;IDSA;DCLCRPDTCRSDWDWO;;;WD)(AU;IDFA;DCLCRPDTCRSDWDWO;;;WD)',
        '(AU;SA;DCLCRPDTCRSDWDWO;;;WD)(AU;FA;DCLCRPDTCRSDWDWO;;;WD)']

# Modify success\failed
if audit == ['True', 'False', 'True', 'True']:
    value = [
        '(AU;OICISA;DCLCRPDTCRSDWDWO;;;WD)(AU;OICIFA;CCDCLCRPDTCRSDWDWO;;;WD)',
        '(AU;OICIIDSA;DCLCRPDTCRSDWDWO;;;WD)(AU;OICIIDFA;CCDCLCRPDTCRSDWDWO;;;WD)',
        '(AU;IDSA;DCLCRPDTCRSDWDWO;;;WD)(AU;IDFA;CCDCLCRPDTCRSDWDWO;;;WD)',
        '(AU;SA;DCLCRPDTCRSDWDWO;;;WD)(AU;FA;CCDCLCRPDTCRSDWDWO;;;WD)']

# Modify success\failed Read success
if audit == ['True', 'True', 'True', 'False']:
    value = [
        '(AU;OIIOSA;CC;;;WD)(AU;OICISA;DCLCRPDTCRSDWDWO;;;WD)(AU;OICIFA;DCLCRPDTCRSDWDWO;;;WD)',
        '(AU;OIIOIDSA;CC;;;WD)(AU;OICIIDSA;DCLCRPDTCRSDWDWO;;;WD)(AU;OICIIDFA;DCLCRPDTCRSDWDWO;;;WD)',
        '(AU;IDSA;CC;;;WD)(AU;IDSA;DCLCRPDTCRSDWDWO;;;WD)(AU;IDFA;DCLCRPDTCRSDWDWO;;;WD)',
        '(AU;SA;CC;;;WD)(AU;SA;DCLCRPDTCRSDWDWO;;;WD)(AU;FA;DCLCRPDTCRSDWDWO;;;WD)']

# Modify success Read success\failed
if audit == ['True', 'True', 'False', 'True']:
    value = [
        '(AU;OIIOSA;CC;;;WD)(AU;OICISA;DCLCRPDTCRSDWDWO;;;WD)(AU;OICIFA;CC;;;WD)',
        '(AU;OIIOIDSA;CC;;;WD)(AU;OICIIDSA;DCLCRPDTCRSDWDWO;;;WD)(AU;OICIIDFA;CC;;;WD)',
        '(AU;IDSA;CC;;;WD)(AU;IDSA;DCLCRPDTCRSDWDWO;;;WD)(AU;IDFA;CC;;;WD)',
        '(AU;SA;CC;;;WD)(AU;SA;DCLCRPDTCRSDWDWO;;;WD)(AU;FA;CC;;;WD)']

# Modify success\failed Read success\failed'
if audit == ['True', 'True', 'True', 'True']:
    value = [
        '(AU;OIIOSA;CC;;;WD)(AU;OICISA;DCLCRPDTCRSDWDWO;;;WD)(AU;OICIFA;CCDCLCRPDTCRSDWDWO;;;WD)',
        '(AU;OIIOIDSA;CC;;;WD)(AU;OICIIDSA;DCLCRPDTCRSDWDWO;;;WD)(AU;OICIIDFA;CCDCLCRPDTCRSDWDWO;;;WD)',
        '(AU;IDSA;CC;;;WD)(AU;IDSA;DCLCRPDTCRSDWDWO;;;WD)(AU;IDFA;CCDCLCRPDTCRSDWDWO;;;WD)',
        '(AU;SA;CC;;;WD)(AU;SA;DCLCRPDTCRSDWDWO;;;WD)(AU;FA;CCDCLCRPDTCRSDWDWO;;;WD)']


# Enum shares and exclude hidden shares
shareresume = 0
sharelist = []
while 1:
    sharedata, total, shareresume = win32net.NetShareEnum(
        targetServer, 2, shareresume)
    for share in sharedata:
        if "$" not in share['netname']:
            sharelist.append(share['netname'])
            print 'Share name - ', share['netname']
    if not shareresume:
        break

# Getting SDDL from file system objects and validate
def getsddl(path):
    fname = path
    sd = win32security.GetFileSecurity(
        fname, win32security.SACL_SECURITY_INFORMATION)
    sddl = win32security.ConvertSecurityDescriptorToStringSecurityDescriptor(
        sd, win32security.SDDL_REVISION_1, win32security.SACL_SECURITY_INFORMATION)
    print path
    print str(sddl)
    return sddl


def validate(wara):
    rootdir = '\\\\' + str(targetServer) + '\\' + wara
    sddl = getsddl(rootdir)
    if str(sddl[2:]) == 'PAI' + value[0]:
        print 'True'
    else:
        print 'FALSE!!!'

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            tgt = os.path.join(subdir, file)
            sddl = getsddl(tgt)
            if str(sddl)[2] == "P" and str(sddl)[5:] == value[3]:
                print 'True'
            elif str(sddl)[2] == "A" and str(sddl)[4:] == value[2]:
                print 'True'
            else:
                print 'FALSE!!!'

    for subdir, dirs, files in os.walk(rootdir):
        for dir in dirs:
            tgt = os.path.join(subdir, dir)
            sddl = getsddl(tgt)
            if str(sddl)[2] == "P" and str(sddl)[5:] == value[0]:
                print 'True'
            elif str(sddl)[2] == "A" and str(sddl)[4:] == value[1]:
                print 'True'
            else:
                print 'FALSE!!!'

for wara in sharelist:
    validate(wara)
