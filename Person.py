import tkinter as tk
from playsound import playsound
import random
import math
import numpy as np
import sys
from PIL import Image, ImageTk

class Cat:
    def __init__(self,namep,canvasp):
        self.x = random.randint(300,600)
        self.y = random.randint(100,900)
        self.theta = random.uniform(0.0,2.0*math.pi)
        self.name = namep
        self.canvas = canvasp
        self.vl = 1.0
        self.vr = 1.0
        self.turning = 0
        self.moving = random.randrange(50,100)
        self.currentlyTurning = False
        self.ll = 20 #axle width
        imgFile = Image.open("person.png")
        imgFile = imgFile.resize((30,30), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(imgFile)
        self.temp_path=None
        self.source=None
        
    def draw(self,canvas):
        body = canvas.create_image(self.x,self.y,image=self.image,tags=self.name)

    def getLocation(self):
        return self.x, self.y

    def transferFunction(self):
        # wandering behaviour
        if self.currentlyTurning==True:
            self.vl = -2.0
            self.vr = 2.0
            self.turning -= 1
        else:
            self.vl = 1.0
            self.vr = 1.0
            self.moving -= 1
        if self.moving==0 and not self.currentlyTurning:
            self.turning = random.randrange(20,40)
            self.currentlyTurning = True
        if self.turning==0 and self.currentlyTurning:
            self.moving = random.randrange(50,100)
            self.currentlyTurning = False
            
    def move(self,canvas,registryPassives,dt):
        if self.vl==self.vr:
            R = 0
        else:
            R = (self.ll/2.0)*((self.vr+self.vl)/(self.vl-self.vr))
        omega = (self.vl-self.vr)/self.ll
        ICCx = self.x-R*math.sin(self.theta) #instantaneous centre of curvature
        ICCy = self.y+R*math.cos(self.theta)
        m = np.matrix( [ [math.cos(omega*dt), -math.sin(omega*dt), 0],                         [math.sin(omega*dt), math.cos(omega*dt), 0],                          [0,0,1] ] )
        v1 = np.matrix([[self.x-ICCx],[self.y-ICCy],[self.theta]])
        v2 = np.matrix([[ICCx],[ICCy],[omega*dt]])
        newv = np.add(np.dot(m,v1),v2)
        newX = newv.item(0)
        newY = newv.item(1)
        newTheta = newv.item(2)
        newTheta = newTheta%(2.0*math.pi) #make sure angle doesn't go outside [0.0,2*pi)
        self.x = newX
        self.y = newY
        self.theta = newTheta        
        if self.vl==self.vr: # straight line movement
            self.x += self.vr*math.cos(self.theta) #vr wlog
            self.y += self.vr*math.sin(self.theta)
        if self.x<150.0:
            self.x=random.randrange(152.0,155.0)
        if self.x>850.0:
            self.x = random.randrange(845.0,848.0)
        if self.y<50.0:
            self.y=random.randrange(52.0,55.0)
        if self.y>600.0:
            self.y = random.randrange(595.0,598.0)
        #self.updateMap()
        canvas.delete(self.name)
        self.draw(canvas)

    def jump(self):
        self.x += random.randint(20,50)
        self.y += random.randint(20,50)
        if self.x<150.0:
            self.x=random.randrange(152.0,155.0)
        if self.x>850.0:
            self.x = random.randrange(845.0,848.0)
        if self.y<50.0:
            self.y=random.randrange(52.0,55.0)
        if self.y>600.0:
            self.y = random.randrange(595.0,598.0)
        #self.updateMap()
        self.canvas.delete(self.name)
        self.draw(self.canvas)

    def bigJump(self):
        self.x += random.randint(50,100)
        self.y += random.randint(50,100)
        if self.x<150.0:
            self.x=random.randrange(152.0,155.0)
        if self.x>850.0:
            self.x = random.randrange(845.0,848.0)
        if self.y<50.0:
            self.y=random.randrange(52.0,55.0)
        if self.y>600.0:
            self.y = random.randrange(595.0,598.0)
        #self.updateMap()
        self.canvas.delete(self.name)
        self.draw(self.canvas)

