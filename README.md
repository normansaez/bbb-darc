bbb-darc
========

BeagleBoneBlack and Darc
------------------------

Ubuntu version:
--------------
BBB-eMMC-flasher-ubuntu-13.04-2013-10-08.img

* wget https://rcn-ee.net/deb/flasher/raring/BBB-eMMC-flasher-ubuntu-13.04-2013-10-08.img.xz
* unzx BBB-eMMC-flasher-ubuntu-13.04-2013-10-08.img
* sudo dd if=BBB-eMMC-flasher-ubuntu-13.04-2013-10-08.img of=/dev/sdX bs=1M

*Expanding File System Partition On A microSD*
   1. use fdisk to delete /dev/mmcblk0p2 partition
   2. create /dev/mmcblk0p2 again using all free space
   3. resize2fs /dev/mmcblk0p2


*Loading the image to eMMc*
   1. Power down the BBB.
   2. Insert the microSD card.
   3. Hold down the BOOT button the on the BBB (this is the on at the same end of the board as the microSD card slot.
   4. Power the board up while still holding down the BOOT button.
   5. You can release the button when all 4 LEDs are lit.
   6. Go away and have a coffee. The process is finished when all 4 LEDs are solidly lit.
   7. Power down the BBB and remove the microSD card. Next time it is
   8. powered up it will boot into Ubuntu.

*Adafruit Version*:
-------------------
* git clone https://github.com/adafruit/adafruit-beaglebone-io-python.git
* git version: f70c915

*set gpio to mode 7*:

See:
* http://www.embedded-things.com/bbb/patching-the-device-tree-compiler-for-ubuntu/

   1. sudo apt-get install build-essential bison flex
   2. git clone http://jdl.com/software/dtc.git/
   3. cd dtc
   4. git reset --hard f8cb5dd94903a5cfa1609695328b8f1d5557367f
   5. wget https://patchwork.kernel.org/patch/1934471/raw/ -O dynamic-symbols.patch
   6. git apply dynamic-symbols.patch
   7. make
   8. sudo cp dtc /usr/local/bin
   9. dtc -O dtb -o <overlay filename> -b 0 -@ <source filename>

Example:
   10. dtc -O dtb -o pinctrl-test-7-00A0.dtbo -b 0 -@ pinmux-test-7.dts 
   11. cp pinctrl-test-7-00A0.dtbo /lib/firmware/
   12. echo pinctrl-test-7 > $SLOTS 

*Useful*:
   1. export SLOTS=/sys/devices/bone_capemgr.9/slots 
   2. export PINS=/sys/kernel/debug/pinctrl/44e10800.pinmux/pins
   3. export PINMUX=/sys/kernel/debug/pinctrl/44e10800.pinmux/pinmux-pins
   4. export PINGROUPS=/sys/kernel/debug/pinctrl/44e10800.pinmux/pingroups


*PYTHONPATH*
* add this ~/bbb-darc/BBBServer to PYTHONPATH

Package to install:
-------------------
* sudo apt-get update
* sudo apt-get install vim python-omniorb omniidl omniidl-python tree omniorb omniorb-nameserver build-essential ntpdate python-dev bison flex screen

*Possible errors*
Traceback (most recent call last):
      File "/home/ubuntu/bbb-darc/BBBServer/server.py", line 212, in <module>
          rootContext = obj._narrow(CosNaming.NamingContext)
        File "/usr/lib/python2.7/dist-packages/omniORB/CORBA.py", line 798, in _narrow
          return _omnipy.narrow(self, repoId, 1)
      omniORB.CORBA.TRANSIENT: CORBA.TRANSIENT(omniORB.TRANSIENT_ConnectFailed, CORBA.COMPLETED_NO)

*Check*
cat /var/log/omniorb-nameserver.log

if you see something like:
Error: parse error in log file '/var/lib/omniorb/omninames-arm.log' at line 1.

It is possible that /var/lib/omniorb/omninames-arm.log is empty.
*Useful*:
   1. cp /var/lib/omniorb/omninames-arm.bak /var/lib/omniorb/omninames-arm.log
   2. reboot machine
   3. check    InitRef = NameService=corbaname::host in /etc/omniORB.cfg

