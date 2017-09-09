# Get registry key

import _winreg

y = _winreg.ConnectRegistry('localhost' , _winreg.HKEY_LOCAL_MACHINE)

x = _winreg.CreateKey(y, 'SECURITY\\Policy\\PolAdtEv')
print x

print _winreg.EnumValue(x, 0)
