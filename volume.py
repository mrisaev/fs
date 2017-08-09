# WMI request template

import wmi

c = wmi.WMI()
wql =  "SELECT * FROM Win32_volume"
for disk in c.query(wql):
    print disk
