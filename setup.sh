#!/bin/bash

echo "Updating system"
sudo apt update
sudo apt upgrade -y

echo "Installing dependancies"
sudo apt install git python3 python3-pip
pip3 install -r requirements.txt

echo -e "\nReddit API setup"
echo "Navigate to https://ssl.reddit.com/prefs/apps/ and create a reddit app"
echo "What is your App Client_ID (hint: string under app name)?: "
read response_id
echo "What is your app Secret?: "
read response_secret
echo "What is your app Name?: "
read response_bot
echo "---"
echo $response_id
echo $response_secret
echo $response_bot

# write respose to config file
$config_file="Scraper_config.py"
cp Scraper_config.py.example $config_file
sed -i "s/CLIENT ID/$response_id/" $config_file
sed -i "s/CLIENT SECRET/$response_secret/" $config_file
sed -i "s/BOT USERNAME/$response_bot/" $config_file


