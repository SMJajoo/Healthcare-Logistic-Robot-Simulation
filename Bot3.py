import tkinter as tk
from playsound import playsound
import random
import math
import numpy as np
import sys
from greedyAstar import *
# from astar import *       #uncomment for distance based algorithm
from Person import *
from Charger import *

class Bot:

    def __init__(self,namep,canvasp,centreX,centreY):
        self.x = centreX
        self.y = centreY
        self.theta = random.uniform(0.0,2.0*math.pi)
        #self.theta = 0
        self.name = namep
        self.ll = 60 #axle width
        self.vl = 4.0
        self.vr = 4.0
        self.battery = 5000
        self.turning = 0
        self.moving = random.randrange(50,100)
        self.currentlyTurning = False
        self.canvas = canvasp
        self.task=[]
        self.temp_path=[]
        self.collision=False
        self.source=False
        self.omegaGiven=False
        self.omega=0
        self.count_down=5
        self.min_obs_dist=100
        self.obstacle=False
        self.itemPicked=False
        self.obstaclesToAvoid=[]
        self.collisionAllowed=False
        self.trigger=20
        self.charging=False
        self.atCharger=False
        self.health=2000
        self.avoidedCollisions=0
        self.damagedItems=[]
        self.totalTasksCompleted=0
    def distance(point1,point2):
        point1 = np.array(point1)
        point2 = np.array(point2)
        return np.linalg.norm(point1-point2)

    def draw(self,canvas):
        self.cameraPositions = []
        for pos in range(10,-11,-5):
            self.cameraPositions.append( ( (self.x + pos*math.sin(self.theta)) + 10*math.sin((math.pi/2.0)-self.theta),                                  (self.y - pos*math.cos(self.theta)) + 10*math.cos((math.pi/2.0)-self.theta) ) )
           
        points = [ (self.x + 10*math.sin(self.theta)) - 10*math.sin((math.pi/2.0)-self.theta),                    (self.y - 10*math.cos(self.theta)) - 10*math.cos((math.pi/2.0)-self.theta),                    (self.x - 10*math.sin(self.theta)) - 10*math.sin((math.pi/2.0)-self.theta),                    (self.y + 10*math.cos(self.theta)) - 10*math.cos((math.pi/2.0)-self.theta),                    (self.x - 10*math.sin(self.theta)) + 10*math.sin((math.pi/2.0)-self.theta),                    (self.y + 10*math.cos(self.theta)) + 10*math.cos((math.pi/2.0)-self.theta),                    (self.x + 10*math.sin(self.theta)) + 10*math.sin((math.pi/2.0)-self.theta),                    (self.y - 10*math.cos(self.theta)) + 10*math.cos((math.pi/2.0)-self.theta)                  ]
        canvas.create_polygon(points, fill="red", tags=self.name)
        # canvas.create_oval(centre1PosX-30,centre1PosY-30,                           centre1PosX+30,centre1PosY+30,                           fill="red",tags=self.name)
        self.sensorPositions = [ (self.x + 10*math.sin(self.theta)) + 15*math.sin((math.pi/2.0)-self.theta),                                  (self.y - 10*math.cos(self.theta)) + 15*math.cos((math.pi/2.0)-self.theta),                                  (self.x - 10*math.sin(self.theta)) + 15*math.sin((math.pi/2.0)-self.theta),                                  (self.y + 10*math.cos(self.theta)) + 15*math.cos((math.pi/2.0)-self.theta)                              ]
    
        centre1PosX = self.x 
        centre1PosY = self.y
        canvas.create_oval(centre1PosX-15,centre1PosY-15,                           centre1PosX+15,centre1PosY+15,                           fill="white",tags=self.name)
        canvas.create_text(self.x,self.y,text=str(self.name),tags=self.name)

        canvas.create_text(self.x,self.y+20,text=str(self.battery),tags=self.name)

        wheel1PosX = self.x - 10*math.sin(self.theta)
        wheel1PosY = self.y + 10*math.cos(self.theta)
        canvas.create_oval(wheel1PosX-3,wheel1PosY-3,                                         wheel1PosX+3,wheel1PosY+3,                                         fill="red",tags=self.name)

        wheel2PosX = self.x + 10*math.sin(self.theta)
        wheel2PosY = self.y - 10*math.cos(self.theta)
        canvas.create_oval(wheel2PosX-3,wheel2PosY-3,                                         wheel2PosX+3,wheel2PosY+3,                                         fill="green",tags=self.name)

        sensor1PosX = self.sensorPositions[0]
        sensor1PosY = self.sensorPositions[1]
        sensor2PosX = self.sensorPositions[2]
        sensor2PosY = self.sensorPositions[3]
        canvas.create_oval(sensor1PosX-3,sensor1PosY-3,                            sensor1PosX+3,sensor1PosY+3,                            fill="yellow",tags=self.name)
        canvas.create_oval(sensor2PosX-3,sensor2PosY-3,                            sensor2PosX+3,sensor2PosY+3,                            fill="yellow",tags=self.name)
        
        for xy in self.cameraPositions:
            canvas.create_oval(xy[0]-2,xy[1]-2,xy[0]+2,xy[1]+2,fill="purple1",tags=self.name)
        for xy in self.cameraPositions:
            canvas.create_line(xy[0],xy[1],xy[0]+100*math.cos(self.theta),xy[1]+100*math.sin(self.theta),fill="light grey",tags=self.name)
        
        if self.itemPicked:
            canvas.create_rectangle(self.x-10,self.y+5, \
                                  self.x+10,self.y+10,outline="black", fill="yellow",tags=self.name)

        if self.charging:
            canvas.create_rectangle(self.x-10,self.y+10, \
                                  self.x+10,self.y+10,outline="black", fill="red",tags=self.name)
    # cf. Dudek and Jenkin, Computational Principles of Mobile Robotics
    def move(self,canvas,registryPassives,dt,demand,destination,collisions):        
        if self.battery>0:
            self.battery -= 1
        if self.battery<=0:
            self.vl = 0
            self.vr = 0

        for rr in registryPassives:
            if isinstance(rr,Charger):
                if self.distanceTo(rr)<80 and self.charging:
                    self.battery += 10
                    rr.using=1
                    if self not in rr.toCharge: 
                        collisions.chargersUsed+=1
                        rr.toCharge.append(self)
                else:
                    rr.using=0
                    if self in rr.toCharge: rr.toCharge.remove(self)

        if self.vl==self.vr:
            R = 0
        else:
            R = (self.ll/2.0)*((self.vr+self.vl)/(self.vl-self.vr))
        if not self.omegaGiven: self.omega = (self.vl-self.vr)/self.ll
        ICCx = self.x-R*math.sin(self.theta) #instantaneous centre of curvature
        ICCy = self.y+R*math.cos(self.theta)
        m = np.matrix( [ [math.cos(self.omega*dt), -math.sin(self.omega*dt), 0],                         [math.sin(self.omega*dt), math.cos(self.omega*dt), 0],                          [0,0,1] ] )
        v1 = np.matrix([[self.x-ICCx],[self.y-ICCy],[self.theta]])
        v2 = np.matrix([[ICCx],[ICCy],[self.omega*dt]])
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
            self.x=random.randrange(152.0,154.0)
            self.vr=0
            self.vl=random.randrange(2.0,4.0)
        if self.x>850.0:
            self.x = random.randrange(844.0,848.0)
            self.vr=0
            self.vl=random.randrange(2.0,4.0)
        if self.y<50.0:
            self.y=random.randrange(52.0,54.0)
            self.vr=0
            self.vl=random.randrange(2.0,4.0)
        if self.y>600.0:
            self.y = random.randrange(594.0,598.0)
            self.vr=0
            self.vl=random.randrange(2.0,4.0)
        # if self.obstacle:
        #     self.vr=0.4
        #     self.vl=0.4
        if self.battery<=0:
            self.vl = 0
            self.vr = 0
        canvas.delete(self.name)
        self.draw(canvas)

    def look(self,registryActives,collisions):
        self.view = [0]*5
        for idx,pos in enumerate(self.cameraPositions):
            for cc in registryActives:
                if cc.name!=self.name: #isinstance(cc,Bot) and 
                    dd = self.distanceTo(cc)
                    scaledDistance = max(400-dd,0)/400
                    ncx = cc.x-pos[0]
                    ncy = cc.y-pos[1]
                    #print(abs(angle-self.theta)%2.0*math.pi)
                    m = math.tan(self.theta)
                    A = m*m+1
                    B = 2*(-m*ncy-ncx)
                    r = 15 #radius
                    C = ncy*ncy - r*r + ncx*ncx 
                    if B*B-4*A*C>=0 and scaledDistance>self.view[idx]:
                        self.view[idx] = scaledDistance
                    if scaledDistance>0.7:
                        # if isinstance(cc,Person):
                        #     cc.jump()
                        self.collision=True
                        if cc not in self.obstaclesToAvoid:
                            self.obstaclesToAvoid.append(cc)
                            if scaledDistance>=0.9:
                                if self.task not in self.damagedItems:
                                    self.damagedItems.append(self.task)
                                collisions.collisions+=1
                                if self.health>0: self.health-=1
        if max(self.view)>0.7:
            self.collision=True
            self.temp_path=[]
            self.obstaclesToAvoid.sort(key= lambda x: self.distanceTo(x))
        else: 
            self.collision=False
            self.obstaclesToAvoid=[]
        return self.view

        
    def pickUpAndPutDown(self,xp,yp):
        self.x = xp
        self.y = yp
        self.canvas.delete(self.name)
        self.draw(self.canvas)
    
    def senseHubs(self, registryPassives):
        signal = []
        for pp in registryPassives:
            if isinstance(pp,Hub):
                lx,ly = pp.getLocation()
                distanceL = math.sqrt( (lx-self.sensorPositions[0])*(lx-self.sensorPositions[0]) +                                        (ly-self.sensorPositions[1])*(ly-self.sensorPositions[1]) )
                distanceR = math.sqrt( (lx-self.sensorPositions[2])*(lx-self.sensorPositions[2]) +                                        (ly-self.sensorPositions[3])*(ly-self.sensorPositions[3]) )
                signal.append(200000/(distanceL*distanceL))
                signal.append(200000/(distanceR*distanceR))
        return signal
    
    def senseDemandLocation(self, registryPassives):
        demandL = 0.0
        demandR = 0.0
        for pp in registryPassives:
            if isinstance(pp,Hub):
                lx,ly = pp.getLocation()
                #print(lx,ly)
                distanceL = math.sqrt( (lx-self.sensorPositions[0])*(lx-self.sensorPositions[0]) +                                        (ly-self.sensorPositions[1])*(ly-self.sensorPositions[1]) )
                distanceR = math.sqrt( (lx-self.sensorPositions[2])*(lx-self.sensorPositions[2]) +                                        (ly-self.sensorPositions[3])*(ly-self.sensorPositions[3]) )
                demandL += 200000/(distanceL*distanceL)
                demandR += 200000/(distanceR*distanceR)
        return distanceL, distanceR
    
    def distanceTo(self,obj):
        xx,yy = obj.getLocation()
        return math.sqrt( math.pow(self.x-xx,2) + math.pow(self.y-yy,2) )

    def collectDirt(self, canvas, registryPassives, count):
        toDelete = []
        for idx,rr in enumerate(registryPassives):
            if isinstance(rr,Dirt):
                if self.distanceTo(rr)<30:
                    canvas.delete(rr.name)
                    toDelete.append(idx)
                    count.itemCollected(canvas)
        for ii in sorted(toDelete,reverse=True):
            del registryPassives[ii]
        return registryPassives
        
    def getLocation(self):
        return self.x, self.y           
    
    def findAPath(self,registryPassives,demand,source):
        path=[]
        list_chrg=[]  
        lx,ly=0,0      
        if not demand:
            for pp in registryPassives:
                if isinstance(pp,Charger):
                    if pp.using==0:
                        lx,ly = pp.getLocation()
                        distanceL = math.sqrt( (lx-self.x)*(lx-self.x) + (ly-self.y)*(ly-self.y))
                        list_chrg.append((distanceL,(lx,ly)))
            if list_chrg:
                list_chrg.sort(key = lambda x: x[0])
                # print(list_chrg)
                lx, ly=list_chrg[0][1][0],list_chrg[0][1][1]

            path=aStarSearch(makeSpecificGrid(int(self.x),int(self.y),lx,ly),int(self.x),int(self.y),lx,ly)
            for i in range(150):
                path.append(path[-1])
                path.append(path[-2])
            # print(path)
        else: 
            path=aStarSearch(makeSpecificGrid(int(self.x),int(self.y),demand[0],demand[1]),int(self.x),int(self.y),demand[0],demand[1])
        

        # for place in path:
        #     new_path=new_path.append((place[0]*100,place[1]*100)) 

        # for place in path:
        #     path.remove(place)
        #     nextPath=aStarSearch(makeSpecificGrid(int(self.x),int(self.y),place[0],place[1]),int(self.x),int(self.y),place[0],place[1])
        #     path.append(nextPath)
        # print(path)
        return path
              
    def transferFunction(self,chargerL, chargerR):
        # wandering behaviour
        if self.currentlyTurning==True and not self.collision:
            self.vl = -3.0
            self.vr = 3.0
            self.turning -= 1
        elif not self.collision:
            self.vl = 2.0
            self.vr = 2.0
            self.moving -= 1
        
        if self.moving==0 and not self.currentlyTurning:
            self.turning = random.randrange(20,40)
            self.currentlyTurning = True
        
        if self.turning==0 and self.currentlyTurning:
            self.moving = random.randrange(50,100)
            self.currentlyTurning = False

        #battery - these are later so they have priority
        # if self.battery<=1100:
        #     if chargerR>chargerL:
        #         self.vl = 2.0
        #         self.vr = -2.0
        #     elif chargerR<chargerL:
        #         self.vl = -2.0
        #         self.vr = 2.0
        #     # else:
        #     #     self.vl = 2.0
        #     #     self.vr = 2.0
        #     if abs(chargerR-chargerL)<chargerL*0.1: #approximately the same
        #         self.vl = 3.0
        #         self.vr = 3.0
        # if chargerL and chargerR:
        #     if chargerL+chargerR>200:
        #         if self.battery<4000:
        #             self.vl = 0.0
        #             self.vr = 0.0
    
    def getAwayFromObstacle(self,dangerThreshold,registryActives,collisions):
        sensors = self.look(registryActives,collisions)
        for element in self.obstaclesToAvoid:
            x=element.x
            y=element.y
            lightL = 0.0
            lightR = 0.0
            distanceL = math.sqrt( (x-self.cameraPositions[0][0])*(x-self.cameraPositions[0][0]) + \
                                               (y-self.cameraPositions[0][1])*(y-self.cameraPositions[0][1]) )
            distanceR = math.sqrt( (x-self.cameraPositions[4][0])*(x-self.cameraPositions[4][0]) + \
                                               (y-self.cameraPositions[4][1])*(y-self.cameraPositions[4][1] ))
            lightL += 200000/(distanceL*distanceL)
            lightR += 200000/(distanceR*distanceR)
        #     if self.battery<600:
            
            
            if abs(lightR-lightL)<lightL*0.1 and self.trigger!=0: #approximately the same
                self.vl = -3.0
                self.vr = 3.0
                element.vl=0.0
                element.vr=0.0
                self.trigger-=1
            elif lightR<lightL and self.trigger!=0:
                self.vl = 3.0
                self.vr = -3.0
                element.vl=0.0
                element.vr=0.0
                self.currentlyTurning=True
                self.trigger-=1
            elif lightR>lightL and self.trigger!=0:
                self.vl = -3.0
                self.vr = 3.0
                element.vl=0.0
                element.vr=0.0
                self.currentlyTurning=True
                self.trigger-=1
            else:
                self.vl = 3.0
                self.vr = 3.0
                self.trigger=20
            self.obstaclesToAvoid.remove(element)
            # if self.health>0: self.health-=1
            # self.avoidedCollisions+=1

        return collisions


        #     if chargerL+chargerR>200 and self.battery<1000:
        #         self.vl = 0.0
        #         self.vr = 0.0
        # self.collisionAllowed=False





    def checkForDanger(self,dangerThreshold,registryActives,collisions):
        if self.collision: print(self.collision," for ", self.name)
        if not self.collision: 
            sensors = self.look(registryActives,collisions)
            if max(sensors)>dangerThreshold:
                if sensors.index(max(sensors))<=2:
                    self.vl=-4.0
                    self.vr=4.0
                else:
                    self.vl=4.0
                    self.vr=-4.0
                # self.moving-=1
                self.temp_path=[]
                self.currentlyTurning=True
            else:
                self.vl=4.0
                self.vr=4.0
                # self.moving=5
                # self.vl=3.0
                # self.vr=3.0
                # self.moving=2
                # self.currentlyTurning=False
        else:
            if self.turning==0:
                self.collision=False
            else: self.turning-=1
            self.temp_path=[]

    # def senseCharger(self, registryPassives):
    #     lightL = 0.0
    #     lightR = 0.0
    #     for pp in registryPassives:
    #         if isinstance(pp,Charger):
    #             lx,ly = pp.getLocation()
    #             distanceL = math.sqrt( (lx-self.sensorPositions[0])*(lx-self.sensorPositions[0]) + \
    #                                    (ly-self.sensorPositions[1])*(ly-self.sensorPositions[1]) )
    #             distanceR = math.sqrt( (lx-self.sensorPositions[2])*(lx-self.sensorPositions[2]) + \
    #                                    (ly-self.sensorPositions[3])*(ly-self.sensorPositions[3]) )
    #             lightL += 200000/(distanceL*distanceL)
    #             lightR += 200000/(distanceR*distanceR)
    #     return lightL, lightR


    def senseCharger(self, registryPassives):
        lightL = 0.0
        lightR = 0.0
        list_chrg=[]
        for pp in registryPassives:
            if isinstance(pp,Charger):
                if pp.using==0:
                    lx,ly = pp.getLocation()
                    distanceL = math.sqrt( (lx-self.sensorPositions[0])*(lx-self.sensorPositions[0]) + \
                                           (ly-self.sensorPositions[1])*(ly-self.sensorPositions[1]) )
                    distanceR = math.sqrt( (lx-self.sensorPositions[2])*(lx-self.sensorPositions[2]) + \
                                           (ly-self.sensorPositions[3])*(ly-self.sensorPositions[3]) )
                    lightL += 400000/(distanceL*distanceL)
                    lightR += 400000/(distanceR*distanceR)
                    list_chrg.append((lightL+lightR,(lightL,lightR)))
        if list_chrg: 
            list_chrg.sort(key = lambda x: x[0])
            lightL, lightR=list_chrg[0][1][0],list_chrg[0][1][1]
        if lightL<1: lightL=lightL*10
        if lightR<1: lightR=lightR*10
        
        return lightL, lightR

def checkDirection(self,dest,registryPassives):
    lightL = 0.0
    lightR = 0.0
    distanceL = math.sqrt( (dest[0]-self.sensorPositions[0])*(dest[0]-self.sensorPositions[0]) + \
                                       (dest[1]-self.sensorPositions[1])*(dest[1]-self.sensorPositions[1]) )
    distanceR = math.sqrt( (dest[0]-self.sensorPositions[2])*(dest[0]-self.sensorPositions[2]) + \
                                       (dest[1]-self.sensorPositions[3])*(dest[1]-self.sensorPositions[3]) )
    lightL += 200000/(distanceL*distanceL)
    lightR += 200000/(distanceR*distanceR)
#     if self.battery<600:
    if lightR>lightL:
        self.vl = 2.0
        self.vr = -2.0
    elif lightR<lightL:
        self.vl = -2.0
        self.vr = 2.0
    elif abs(lightR-lightL)<lightL*0.1: #approximately the same
        self.vl = 4.0
        self.vr = 4.0
    else:
        self.vl = -4.0
        self.vr = -4.0
    # chargerIntensityL, chargerIntensityR = self.senseCharger(registryPassives)
    # self.transferFunction(chargerIntensityL, chargerIntensityR)
#     if chargerL+chargerR>200 and self.battery<1000:
#         self.vl = 0.0
#         self.vr = 0.0
