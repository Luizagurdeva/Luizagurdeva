# Christiansø_SmartBin_Group1

This script was created based on the assignment we were given by KEA in Module 8.

The purpose of the script is to depict real-time data through a Flask WebServer and update MySQL simultaneously.

## Requirements

1. Install Raspberry Pi OS LITE on the SD card
2. Create an empty SSH file and “wpa_supplicant.conf” containing a code for our network connection
3. After making sure that both files have no end-name extensions, transfer both to the SD card before booting up the RPi.
4. After successfully connecting it to the network, write “ping raspberrypi.local” to find the ip address and then “ssh pi@ip-address” to access it. While accessing it, the password to the raspberry is 'raspberry'.
5. Make sure all modules needed are installed in order to make the script run on the Raspberry Pi:

sudo apt-get update
sudo apt-get install python3
sudo apt install python3-pip
sudo pip3 install mysql-connector-python
sudo apt install mariadb-server
sudo apt-get install python3-flask
sudo apt install python3-gpiozero

6. Sometimes before running the file the command “export FLASK_APP=wasteflask1.py” has to be written, since we need to provide an application environment.

7. To run the flask app on the RPi the right directory has to be chosen by writing “cd trashbin” and then “sudo python3 wasteflask1.py”.


## Authors:

* Luiza Gardeva
* Romana Macejkova
* Madalina Croitoru
* Sara Eklund
* Stefan Alexandru
* Edvards Banka
* Britt Ferket
