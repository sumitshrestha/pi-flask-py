
from flask import Flask, render_template, send_file
import os
import time
import pygame
import pygame.camera
from pygame.locals import *
import io
from PIL import Image
from io import StringIO, BytesIO
from flask import Response

#cam setup
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0],(1920,1080))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/project')
def project():
    uptime = os.popen("uptime").readline()  
    temp = os.popen("vcgencmd measure_temp").readline()
    return render_template('project.html', temp=temp, uptime=uptime)

@app.route('/videoMonitor')
def videoMonitor():
    cam.start()    
    img = cam.get_image()
    cam.stop()
    data = pygame.image.tostring(img, 'RGBA')
    im = Image.frombytes("RGBA",(1920,1080),data)    
    imgByteArr = io.BytesIO()
    im.save(imgByteArr, format='PNG')
    w=imgByteArr.getvalue()     
    return w, 200, {'content-type':'image/png; charset=utf-8;'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    


