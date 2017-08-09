import os
import sys
import random
import string
import shutil
import win32security
import pywintypes
import win32file
import win32net
import win32netcon
import win32api
import win32con
import ntsecuritycon

a = sys.argv[1]

def help():
    print ('dc - create folders: dc 5 path')
    print ('fc - create empty .txt files: fc 5 path [name]')
    print ('fwc - create .txt with random symbols inside: fwc 5 path [name]')
    print ('rm - remove .txt files or folders: rm 5 path')
    print ('rn - rename files or folders: rn path [oldname] [newname]')
    print ('o - open handle on files: o 5 path [name]')
    print ('ls - list folder: ls path')
    print ('mv - move files or folders: mv spath+name dpath')
    print ('shadd - share folder and set Full access for 2 users: shadd folder-path servername user1 user2')
    print ('shaddc - share given number of folders and set Full access for 2 users: shaddc 10 folder-path servername user1 user2')
    print ('shdel - remove share: shdel servername sharename')
    print ('dacl - set Full access NTFS ACL for 2 users: dacl object-path user1 user2')
    print ('hl - open handle on file with parameter: openh 5 filepath CREATE_ALWAYS\CREATE_NEW\OPEN_ALWAYS\OPEN_EXISTING\TRUNCATE_EXISTING')
    print ('at - set object attribute: at name h\\r\\n\\t\\s\\i\\a')
    print ('ace - add full for 1 user: ace 5 path user')
    print ('enumsh - enumerate shares on server: enumsh servername')
    print ('shdcaddc - add number of shares and set Full access for 2 users: shdcaddc 10 share-path folder-path servername user1 user2')

def dcreate():
    y = 1
    x = sys.argv[2]
    x = int(x)+1
    while y<x:
        print (sys.argv[3] + 'f' + str(y))
        os.makedirs(sys.argv[3] + 'f' + str(y))
        y = y + 1


def fcreate():
    y = 1
    x = sys.argv[2]
    x = int(x)+1
    while y <x:
        print(sys.argv[3] + 't' + str(y) + '.txt', 'w')
        f = open(sys.argv[3] + 't' + str(y) + '.txt', 'w')
        y = y + 1
        f.close


def fwcreate():
    y = 1
    x = sys.argv[2]
    x = int(x)+1
    while y < x:
        t = ''
        r = random.randint(30, 4000)
        f = open(sys.argv[3] + 't' + str(y) + '.txt', 'w')
        t = ''.join([random.choice(string.letters) for i in xrange(r)])
        f.write(t)
        y = y + 1
        f.close


def remove():
    y = 1
    q = sys.argv[2]
    x = sys.argv[3]
    while y < q:
        if os.path.exists(x + str(y)):
            print (x + str(y))
            os.rmdir(x + str(y))
            y = y +1
        else:
            if os.path.isfile(x + str(y) + '.txt'):
                print (x + str(y) + '.txt')
                os.remove(x + str(y) + '.txt')
                y = y+1
            else:
                break


def rename():
    y = 1
    q = sys.argv[2]
    x = sys.argv[3]
    z = sys.argv[4]
    n = sys.argv[5]
    while y < int(q)+1:
        if os.path.isfile(x + z + str(y) + '.txt'):
            print (x + z + str(y) + '.txt', x + n + str(y) + '.txt')
            os.rename(x + z + str(y) + '.txt', x + n + str(y) + '.txt')
        if os.path.exists(x + z + str(y)):
            print (x + z + str(y), x + n + str(y))
            os.rename(x + z + str(y), x + n + str(y))
        y = y + 1


def ropen():
    y = 1
    q = sys.argv[2]
    while y < int(q):
        f = open(sys.argv[3] + sys.argv[4] + str(y) + '.txt', 'r')
        f.read(1)
        y = y + 1
        f.close()


def move():
    y=1
    while os.path.isfile(sys.argv[2] + str(y) + '.txt') == True:
        shutil.move(sys.argv[2] + str(y) + '.txt', sys.argv[3])
        y=y+1
        print y
    y=1
    while os.path.exists(sys.argv[2]+str(y)) == True:
        shutil.move(sys.argv[2] + str(y), sys.argv[3])
        y=y+1
        print y


def createSD(userName1, userName2):
    sd = pywintypes.SECURITY_DESCRIPTOR()
    sidUser1 = win32security.LookupAccountName('nadc', userName1)[0]
    sidUser2 = win32security.LookupAccountName('nadc', userName2)[0]
    #sidCreator = pywintypes.SID()
    # sidCreator.Initialize(ntsecuritycon.SECURITY_CREATOR_SID_AUTHORITY, 1)
    # sidCreator.SetSubAuthority(0, ntsecuritycon.SECURITY_CREATOR_OWNER_RID)
    acl = pywintypes.ACL()
    acl.AddAccessAllowedAce(win32file.FILE_ALL_ACCESS, sidUser1)
    acl.AddAccessAllowedAce(win32file.FILE_ALL_ACCESS, sidUser2)
    #acl.AddAccessAllowedAce(win32file.FILE_ALL_ACCESS, sidCreator)
    sd.SetSecurityDescriptorDacl(1, acl, 0)
    return sd


def addshare():
    fileName = sys.argv[2]
    server = sys.argv[3]
    userId1 = sys.argv[4]
    userId2 = sys.argv[5]
    sd = createSD(userId1, userId2)
    fname = os.path.split(fileName)

    shinfo = {}
    shinfo['netname'] = fname[1]
    shinfo['type'] = win32netcon.STYPE_DISKTREE
    shinfo['remark'] = ''
    shinfo['permissions'] = 0
    shinfo['max_uses'] = -1
    shinfo['current_uses'] = 0
    shinfo['path'] = fileName
    shinfo['passwd'] = ''
    shinfo['security_descriptor'] = sd
    win32net.NetShareAdd(server, 502, shinfo)

def addsharecycl():
    q = sys.argv[2]
    fileName = sys.argv[3]
    server = sys.argv[4]
    userId1 = sys.argv[5]
    userId2 = sys.argv[6]
    sd = createSD(userId1, userId2)
    fname = os.path.split(fileName)

    x = 1
    while x<int(q)+1:
        shinfo = {}
        shinfo['netname'] = fname[1] + str(x)
        shinfo['type'] = win32netcon.STYPE_DISKTREE
        shinfo['remark'] = ''
        shinfo['permissions'] = 0
        shinfo['max_uses'] = -1
        shinfo['current_uses'] = 0
        shinfo['path'] = fileName + str(x)
        shinfo['passwd'] = ''
        shinfo['security_descriptor'] = sd
        win32net.NetShareAdd(server, 502, shinfo)
        x=x+1


def sharedel():
    server = sys.argv[2]
    shname = sys.argv[3]
    win32net.NetShareDel(server, shname)


def dacl():
    fileName = sys.argv[2]
    userId1 = sys.argv[3]
    userId2 = sys.argv[4]
    sd = createSD(userId1, userId2)
    win32security.SetFileSecurity(fileName, win32security.DACL_SECURITY_INFORMATION, sd)

def hl():
    y = 1
    q = sys.argv[2]
    path = sys.argv[3]
    while y < int(q)+1:
        fname = (path + str(y) + '.txt')
        print fname
        hand = win32file.CreateFile(fname, win32file.GENERIC_READ, win32file.FILE_SHARE_DELETE, None, win32file.OPEN_EXISTING, 128, None)
        y = y + 1

def addace():
    q = sys.argv[2]
    fn = sys.argv[3]
    userName1 = sys.argv[4]
    y = 1
    sidUser1 = win32security.LookupAccountName('nadc', userName1)[0]

    while y < int(q)+1:
        fname = (fn + str(y) + '.txt')
        sd = win32security.GetFileSecurity(fname, win32security.DACL_SECURITY_INFORMATION)
        dacl = sd.GetSecurityDescriptorDacl()
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntsecuritycon.FILE_ALL_ACCESS, sidUser1)
        sd.SetSecurityDescriptorDacl(1, dacl, 0)
        win32security.SetFileSecurity(fname, win32security.DACL_SECURITY_INFORMATION, sd)
        y = y +1


def at():
    fname = sys.argv[2]
    attr = sys.argv[3]
    if attr == 'h':
        win32api.SetFileAttributes(fname, win32con.FILE_ATTRIBUTE_HIDDEN),
    elif attr == 'i':
        win32api.SetFileAttributes(fname, win32con.FILE_ATTRIBUTE_NOT_CONTENT_INDEXED),
    elif attr == 'r':
        win32api.SetFileAttributes(fname, win32con.FILE_ATTRIBUTE_READONLY),
    elif attr == 's':
        win32api.SetFileAttributes(fname, win32con.FILE_ATTRIBUTE_SYSTEM),
    elif attr == 't':
        win32api.SetFileAttributes(fname, win32con.FILE_ATTRIBUTE_TEMPORARY)
    elif attr == 'n':
        win32api.SetFileAttributes(fname, win32con.FILE_ATTRIBUTE_NORMAL)
    elif attr == 'a':
        win32api.SetFileAttributes(fname, win32con.FILE_ATTRIBUTE_ARCHIVE)
    else:
        print 'wrong attribute'


def ls():
    p = os.listdir(sys.argv[2])
    print p

def enumsh():
    shareresume=0
    x = sys.argv[2]
    while 1:
        sharedata, total, shareresume = win32net.NetShareEnum(x, 2, shareresume)
        for share in sharedata:
            print(" %(netname)s (%(path)s):%(remark)s - in use by %(current_uses)d users type %(type)s" % share)
        if not shareresume:
            break

def shdcaddc():
    y = 1
    x = sys.argv[2]
    x = int(x)+1
    while y<x:
        print (sys.argv[3] + 'r' + str(y))
        os.makedirs(sys.argv[3] + 'r' + str(y))
        y = y + 1

    filePath = sys.argv[4]
    server = sys.argv[5]
    userId1 = sys.argv[6]
    userId2 = sys.argv[7]
    sd = createSD(userId1, userId2)
    y = 1
    while y<x:
        shinfo = {}
        shinfo['netname'] ='r' + str(y)
        shinfo['type'] = win32netcon.STYPE_DISKTREE
        shinfo['remark'] = ''
        shinfo['permissions'] = 0
        shinfo['max_uses'] = -1
        shinfo['current_uses'] = 0
        shinfo['path'] = filePath + 'f' + str(y)
        shinfo['passwd'] = ''
        shinfo['security_descriptor'] = sd
        win32net.NetShareAdd(server, 502, shinfo)
        y=y+1

if a == 'dc':
    dcreate()
if a == 'fc':
    fcreate()
if a == 'fwc':
    fwcreate()
if a == 'rm':
    remove()
if a == 'rn':
    rename()
if a == 'o':
    ropen()
if a == 'ls':
    ls()
if a == 'mv':
    move()
if a == 'shadd':
    addshare()
if a == 'shaddc':
    addsharecycl()
if a == 'shdel':
    sharedel()
if a == 'dacl':
    dacl()
if a == 'hl':
    hl()
if a == 'at':
    at()
if a == '?':
    help()
if a == 'ace':
    addace()
if a == 'enumsh':
    enumsh()
if a == 'shdcaddc':
    shdcaddc()