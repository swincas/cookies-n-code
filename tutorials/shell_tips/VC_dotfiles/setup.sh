#!/bin/bash

echo " "
echo "------------------"
echo "SETING UP DOTFILES"
echo "------------------"
echo " "


########################################

#  Use hidden files
shopt -s dotglob

# Find the location that this script is being run
LOC="`pwd`"

# Create directory to store previous dotfiles as a backup
OLD_DOTS=~/.old_dotfiles

if [ ! -d $OLD_DOTS ]; then
    echo "NOT FOUND:" $OLD_DOTS
    echo "CREATING ~/.old_dotfiles"
    mkdir $OLD_DOTS
    echo " "
else
    echo "FOUND EXISTING:" $OLD_DOTS
    echo " "
fi

# Create symbolic links to files
DIR=$LOC/files
for FILE in $DIR/*; do
    BASE=`basename $FILE` # BASE = the name of the file
    echo $BASE

    # If the dotfile already exists in home
    # move the file to .old_dotfiles
    if [ -e ~/$BASE ]; then
        echo "FOUND $BASE"
        echo "Moving $BASE to $OLD_DOTS"
        mv ~/$BASE $OLD_DOTS
    fi

    ln -s $FILE ~/$BASE  # Symlink to home directory
    echo "Created $BASE symlink"
    echo " "
done
