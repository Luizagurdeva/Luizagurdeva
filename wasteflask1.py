#Write this in the terminal 'export FLASK_APP=wasteflask.py'
#Here we import all the modules and libraries we need for the code to run properly
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify, Response
import mysql.connector
import ssl
import datetime
import io
import csv
import pymysql
from flaskext.mysql import MySQL
from multiprocessing import Process
import RPi.GPIO as GPIO
import time
from gpiozero import Buzzer, LED
from time import sleep
from flask_mail import Mail, Message

#after importing the RPi.GPIO module, we set our GPIO numbering mode.
GPIO.setmode(GPIO.BCM)

#Here we define each pin with each sensor from the board
GPIO_TRIGGER = 18
GPIO_ECHO = 17
buzzer = Buzzer(26)
green = LED(21)
red = LED(13)

#That's a function which sets a port/pin as an output and input (OUT & IN)
def setup():

    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

#MYSQL configurations, we need this in order to connect to our MySQL Workbench
#We use local host ip address
mydb = mysql.connector.connect(
host="127.0.0.1",
user="wasteuser",
password="waste",
database="wastedb")
mydb.autocommit = True

app = Flask(__name__)
app.secret_key = "wasteflask"


#converting list to a string

def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += convertTuple(ele)

    # return string
    return str1

def convertTuple(tup):
    example = ""
    for item in tup:
        example = example + str(item)

    return example

mycursor =mydb.cursor()
#MYSQL Configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'wasteuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'waste'
app.config['MYSQL_DATABASE_DB'] = 'wastedb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


#Decorator is a structural design pattern that lets you attach new behaviors to objects
#App route is a decorator that Flask provides to assign URLs in our app to functions easily.
@app.route("/database")
def data():
    setup()
    mycursor.execute("SELECT * FROM TrashBins")
    #maybe try to connect email to notify
#Here we have selected all data from our table and we fetch all it all
    data = mycursor.fetchall()
    return convertTuple(data)



@app.route('/download')
def downloading():
	return render_template('download.html')


@app.route('/download/report/csv')
def download_report():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT TrashBinID, Fullness, Address, Location, City FROM TrashBins")
        result = cursor.fetchall()

        output = io.StringIO()
        writer = csv.writer(output)

        line = ['TrashBinID, Fullness, Address, Location, City']
        writer.writerow(line)

        for row in result:
            line = [str(row['TrashBinID']) + ',' + row['Fullness'] + ',' + row['Address'] + ',' + row['Location'] + ',' + row['City']]
            writer.writerow(line)

        output.seek(0)

        return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=waste_report.csv"})
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()




#Here we create another route for our website, which containts a function
#which calculates the distance from the sensor
@app.route('/')
def index():
    setup()
    dis = monitoring()
    sensorReading = str(dis["distance"])
    #before it was 24
    percent = (dis['distance']-3)/.18

#red and gray line stand for the indicator on our web flask server (borders)
    red_line = round(percent*2.6)
    gray_line = 260-red_line
#here we update the mysql database with real-time changes in the data from our sensor
    mycursor.execute("UPDATE TrashBins SET Fullness =" + sensorReading + " WHERE TrashBinID = 1;")

#Render_template returns the html page index1
    return render_template('index1.html', red_line=red_line, gray_line=gray_line)

#another route which contains all the sensor activation functions
@app.route("/monitoring", methods=["POST", "GET"])
def monitoring():
    setup()
    distance = 0
    while True:
        GPIO.output(GPIO_TRIGGER, False)
        time.sleep(2)


        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)


        while GPIO.input(GPIO_ECHO)==0:
            pulseStart = time.time()


        while GPIO.input(GPIO_ECHO)==1:
            pulseEnd = time.time()

        pulseDuration = pulseEnd - pulseStart

        distance = round(pulseDuration * 17150 , 2)
        print(distance)

    #if the distance is bigger than 5cm then pin 21(green light) is activated
    #and the rest is off
        if distance > 5:
            GPIO.output(21,GPIO.HIGH)
            GPIO.output(26,GPIO.LOW)
            GPIO.output(13,GPIO.LOW)
            return ({'Status':1, "distance":distance})
#if distance is smaller than 5 cm then pin 13,26 (red light & buzzer) are activated
        if distance < 5:
            time.sleep(1)
            GPIO.output(13,GPIO.HIGH)
            GPIO.output(26,GPIO.HIGH)
            GPIO.output(21,GPIO.LOW)
            sleep(1)
            GPIO.output(26, False)
            return ({'Status':2,"distance":distance})

        else:
            GPIO.output(26,GPIO.LOW)
            GPIO.output(13,GPIO.LOW)

            return ({'Status':0,'distance':distance})
            sleep(1)



            return render_template("index1.html")




if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0', threaded=True)
