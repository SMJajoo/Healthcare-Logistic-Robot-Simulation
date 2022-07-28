import tkinter as tk
from playsound import playsound
import random
import math
import numpy as np
import sys

class Charger:
    def __init__(self,namep,x,y,using):
        self.centreX = x
        self.centreY = y
        self.name = namep
        self.using=using
        self.toCharge=[]
        
    def draw(self,canvas):
        body = canvas.create_oval(self.centreX-10,self.centreY-10, \
                                  self.centreX+10,self.centreY+10, \
                                  fill="gold",tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY