# Control state and snapshots of vmWare virtual machines 

from pyVmomi import vim
from pyVmomi import vmodl
from pyVim.connect import SmartConnect, Disconnect
from pyVim.task import WaitForTask
import atexit
import argparse
import sys
import time
import ssl

def main():


   try:
      vmnames = 'vmName'
      if not len(vmnames):
         print("No virtual machine specified for poweron")
         sys.exit()

      si = None
      context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
      context.verify_mode = ssl.CERT_NONE
      try:
         si = SmartConnect(host='ESXhost',
                           user='root',
                           pwd='PASSWORD',
                           port='443',
                           sslContext=context)
      except IOError:
         pass
      if not si:
         print("Cannot connect to specified host using specified username and password")
         sys.exit()

      atexit.register(Disconnect, si)

      content = si.content
      objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.VirtualMachine],
                                                        True)
      vmList = objView.view
      objView.Destroy()


      snapshot_name = 'snapshotName'
      for vm in vmList:
        if vm.name in vmnames:
            snapshots = vm.snapshot.rootSnapshotList
            for snapshot in snapshots:
                if snapshot_name == snapshot.name:
                    snap_obj = snapshot.snapshot
                    print ("Reverting snapshot ", snapshot.name)
                    WaitForTask(snap_obj.RevertToSnapshot_Task())
                    time.sleep(5)
      task = [vm.PowerOn() for vm in vmList if vm.name in vmnames]
      WaitForTask(task)
      print("Virtual Machine(s) have been powered on successfully")
   except vmodl.MethodFault as e:
      print("Caught vmodl fault : " + e.msg)
   except Exception as e:
      print("Caught Exception : " + str(e))

# Start program
if __name__ == "__main__":
   main()

