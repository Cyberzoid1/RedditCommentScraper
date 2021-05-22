#!/bin/bash

echo "Updating system"
sudo apt update
sudo apt upgrade -y

echo -e "\nInstalling dependancies"
sudo apt install git python3 python3-pip

echo -e "\nInstalling python dependancies"
pip3 install -r requirements.txt

echo -e "\n\nReddit API setup"
echo "Navigate to https://ssl.reddit.com/prefs/apps/ and create a reddit app"
echo -e "\nWhat is your App Client_ID (hint: string under app name)?: "
read response_id
echo -e "\nWhat is your app Secret?: "
read response_secret
echo -e "\nWhat is your app Name?: "
read response_bot


# write respose to config file
config_file="Scraper_config.py"
cp -v Scraper_config.py.example "$config_file"
sed -i "s/CLIENT ID/$response_id/" $config_file
sed -i "s/CLIENT SECRET/$response_secret/" $config_file
sed -i "s/BOT USERNAME/$response_bot/" $config_file


# Finalize
echo -e "\n\nSetup and configuration complete"
echo "Configs can be reviewed in the $config_file file"
echo -e "\nUsage:"
echo "python3 Scraper.py <thread_id>"