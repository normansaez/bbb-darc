cp -v bashrc  ~/.bashrc
cp -v gitconfig ~/.gitconfig
cp -v pythonrc ~/.pythonrc
cp -v vimrc ~/.vimrc
if [ "$USER" = "root" ]; then
    cp -v sudoers /etc/sudoers
fi
