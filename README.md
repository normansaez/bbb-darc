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

*Loading the image*
   1. Power down the BBB.
   2. Insert the microSD card.
   3. Hold down the BOOT button the on the BBB (this is the on at the same end of
   4. the board as the microSD card slot.
   5. Power the board up while still holding down the BOOT button.
   6. You can release the button when all 4 LEDs are lit.
   7. Go away and have a coffee. The process is finished when all 4 LEDs are solidly lit.
   8. Power down the BBB and remove the microSD card. Next time it is
   9. powered up it will boot into Ubuntu.

*Adafruit Version*:
-------------------
* git clone https://github.com/adafruit/adafruit-beaglebone-io-python.git
* git version: f70c915
