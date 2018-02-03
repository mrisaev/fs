# Get given build from share using impersonation and quiet install it in lab machine

import sys, os, shutil, win32security, subprocess

build = sys.argv[1]
path = '\\\\builderShare\\CurrentVersion\\%s\\WIX Setup\\Release\\en-us\\product.msi' % build
x = win32security.LogonUser('user', 'domain.local', 'PASSWORD', win32security.LOGON32_LOGON_NEW_CREDENTIALS,win32security.LOGON32_PROVIDER_DEFAULT )
win32security.ImpersonateLoggedOnUser(x)
shutil.copyfile(path, '..\\product.msi')
y = win32security.LogonUser('labUser', 'labMachineName', 'PASSWORD', win32security.LOGON32_LOGON_NEW_CREDENTIALS,win32security.LOGON32_PROVIDER_DEFAULT )
win32security.ImpersonateLoggedOnUser(y)
proc = subprocess.Popen('..\\product.msi /qn /l* ..\\1.log', shell=True)
proc.wait()
