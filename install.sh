#!/bin/bash
# License : GPL v3.0
# Created by Saman Ebrahimnezhad .

function menu {
	echo "Which distro are you using?"
	echo -e "	[\033[1;33m1\033[0m] Debian-based(\033[0;33mUbuntu\033[0m, \033[1;32mMint\033[0m ...)"
	echo -e "	[\033[1;33m2\033[0m] Redhat-based(\033[1;31mRHEL\033[0m, \033[1;34mFedora\033[0m ...)"
	echo "	[3] Other"
	echo -n "> "
	read input

	if [ $input -eq '1' ];then
		sudo apt install python3
	elif [ $input -eq '2' ];then
		sudo yum install python3
	else
		echo -e "[\033[0;31m-\033[0m] Install 'python3' on your distro"
	fi
}

echo
echo -e "\033[1;34m _  _ ___ _____ ___ ___ _____ "
echo -e "| \| | __|_   _/ __| __|_   _|"
echo -e "| .\` | _|  | || (_ | _|  | |  "
echo -e "|_|\_|___| |_| \___|___| |_|  "
echo -e "\033[0m"

echo -n "Are you installing netget for the first time? [Y,n]> "

read answer

if [[ "$answer" != "N" && "$answer" != 'n' ]];then
	menu
	sudo mkdir /usr/share/netget
fi

sudo cp bash/netget /bin/

sudo cp core/*.py /usr/share/netget/

echo -e "[\033[0;32m+\033[0m] Done! Just type netget..."
