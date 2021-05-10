from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import water
import os
import auto_light
import auto_fan

app = Flask(__name__)

def template(title = "HELLO!", text = ""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate

@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

@app.route("/last_watered")
def check_last_watered():
    templateData = template(text = water.get_last_watered())
    return render_template('main.html', **templateData)

@app.route("/sensor")
def action():
    status = water.get_status()
    message = ""
    if (status == 1):
        message = "Water me please!"
    else:
        message = "I'm a happy plant"

    templateData = template(text = message)
    return render_template('main.html', **templateData)

@app.route("/water")
def action2():
    water.pump_on()
    templateData = template(text = "Watered Once")
    return render_template('main.html', **templateData)

@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Auto Watering On")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text = "Already running")
                    running = True
            except:
                pass
        if not running:
            os.system("python3 auto_water.py&")
    else:
        templateData = template(text = "Auto Watering Off")
        os.system("pkill -f water.py")

    return render_template('main.html', **templateData)

#For Light
@app.route("/auto/light/<toggle>")
def auto_light(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Auto Light On")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_light.py':
                    templateData = template(text = "Already running")
                    running = True
            except:
                pass
        if not running:
            os.system("python3 auto_light.py&")
    else:
        templateData = template(text = "Auto Light Off")
        os.system("pkill -f auto_light.py")
        os.system("python3 light_off.py&")
    return render_template('main.html', **templateData)

@app.route("/light/off")
def turn_off_light():
    os.system("python3 light_off.py&")
    templateData = template(text = "Light off")
    return render_template('main.html', **templateData)

#For Fan
@app.route("/auto/fan/<toggle>")
def auto_fan(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Auto Fan On")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_fan.py':
                    templateData = template(text = "Already running")
                    running = True
            except:
                pass
        if not running:
            os.system("python3 auto_fan.py&")
    else:
        templateData = template(text = "Auto Fan Off")
        os.system("pkill -f auto_fan.py")
        os.system("python3 fan_off.py&")
    return render_template('main.html', **templateData)

@app.route("/fan/off")
def turn_off_fan():
    os.system("python3 fan_off.py&")
    templateData = template(text = "Fan off")
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='192.168.0.40', port=5680, debug=True)     #IP Address of Raspberry Pi 