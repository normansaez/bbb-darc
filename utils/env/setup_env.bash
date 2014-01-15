cp -v bashrc  ~/.bashrc
cp -v gitconfig ~/.gitconfig
cp -v pythonrc ~/.pythonrc
cp -v vimrc ~/.vimrc
if [ "$USER" = "root" ]; then
    cp -v sudoers /etc/sudoers
    cp -v interfaces /etc/network/interfaces
#    echo "echo pinctrl-test-7 > /sys/devices/bone_capemgr.9/slots" > /etc/rc.local 
fi
