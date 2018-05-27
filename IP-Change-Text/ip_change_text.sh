#! /bin/bash

HOME=$(dig +short myip.opendns.com @resolver1.opendns.com)
PUBLIC_URL=$(cat .Public_URL)
PUBLIC=$(dig +short $PUBLIC_URL)
KEY=$(cat .Textbelt_Key)
PHONE=$(cat .Phone_Number)

if [[ "$HOME" = "$PUBLIC" ]]; then
	curl http://textbelt.com/text -d number=$PHONE -d message='The IP Addresses are the same' -key -d key=$KEY > /dev/null 2>&1
    systemctl stop sabnzbd
	systemctl stop deluged
fi


