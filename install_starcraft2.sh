#!/bin/bash

confirm() {
    # call with a prompt string or use a default
    echo
    read -r -p "${1:-Do you wish to continue? [y/N]} " response
    case "$response" in
        [yY][eE][sS]|[yY])
            true
            ;;
        *)
            false
            ;;
    esac
}

yellow() {
    printf "\033[0;33m$*\033[0m\n"
}


echo
echo
yellow "StarCraftII Installer"
if [ -e $HOME/StarCraftII ]; then
    echo "StarCraftII is already installed in ~/StarCraftII"
    echo "Do you wish to re-install StarCraftII?"
    confirm || exit
    echo "Moving ~/StarCraftII to ~/StarCraftII.bak"
    mv $HOME/StarCraftII $HOME/StarCraftII.bak
else
    echo "StarCraftII is not installed"
    echo "Installer will download StarCraftII to `pwd`/StarCraftII"
    echo "Installer will add symbolic link $HOME/StarCraftII --> `pwd`/StarCraftII"
    confirm || exit
fi

if [ ! -z "$SC2_CACHE" ]; then
    echo "Copying pre-downloaded StarCraft files from  $SC2_CACHE ..."
    rsync -v $SC2_CACHE/*.zip .
fi

yellow "Performing StarCraftII installation..."

wget -nc http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.0.2.zip
unzip -P iagreetotheeula SC2.4.0.2.zip
ln -s $(pwd)/StarCraftII $HOME/StarCraftII

unzip mini_games.zip -d StarCraftII/Maps/
unzip -P iagreetotheeula Melee.zip -d StarCraftII/Maps/
unzip -P iagreetotheeula Ladder2017Season3.zip -d StarCraftII/Maps/
unzip -P iagreetotheeula Ladder2017Season2.zip -d StarCraftII/Maps/
unzip -P iagreetotheeula Ladder2017Season1.zip -d StarCraftII/Maps/

yellow "StarCraftII is installed to `pwd`/StarCraftII"
