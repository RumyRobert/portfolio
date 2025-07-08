import random
import os

movement_distance_min = [-10, 10]
movement_distance_max = [-700, 700]

def setNUMBER_OF_STEPS():
    global NUMBER_OF_STEPS
    NUMBER_OF_STEPS = random.randint(6, 15) #Number of how many steps each Robot will have


setNUMBER_OF_STEPS()

def generate_class_file(class_name, radar_lock, movement_behaviour, onTargetSpotted_behaviour, botCollision_behaviour, file_name):
    movement_code = '\n        '.join(movement_behaviour)

    class_template = f'''
#! /usr/bin/python
# -*- coding: utf-8 -*-

import math
from robot import Robot  # Import a base Robot

class {class_name}(Robot):  # Create a Robot

    def init(self):  # NECESARY FOR THE GAME   To initialyse your robot

        # Set the bot color in RGB
        self.setColor(0, 200, 100)
        self.setGunColor(200, 200, 0)
        self.setRadarColor(255, 60, 0)
        self.setBulletsColor(0, 200, 100)

        # get the map size
        size = self.getMapSize()  # get the map size
        self.radarVisible(True)  # show the radarField
        
        #start_of_radar
        self.lockRadar("{radar_lock}")
        self.setRadarField("{random.choice(["normal", "large", "thin", "round"])}")
        #end_of_radar

    #start_of_movement
    def run(self):  # NECESARY FOR THE GAME  main loop to command the bot
        {movement_code}
    #end_of_movement
    
    #start_of_collision
    def onHitByRobot(self, robotId, robotName):
        {botCollision_behaviour}
    def onRobotHit(self, robotId, robotName):  # when My bot hit another
        {botCollision_behaviour}
    #end_of_collision

    def sensors(self):  # NECESARY FOR THE GAME
        """Tick each frame to have datas about the game"""

        pos = self.getPosition()  # return the center of the bot
        x = pos.x()  # get the x coordinate
        y = pos.y()  # get the y coordinate

        angle = self.getGunHeading()  # Returns the direction that the robot's gun is facing
        angle = self.getHeading()  # Returns the direction that the robot is facing
        angle = self.getRadarHeading()  # Returns the direction that the robot's radar is facing
        list = self.getEnemiesLeft()  # return a list of the enemies alive in the battle
        for robot in list:
            id = robot["id"]
            name = robot["name"]
            # each element of the list is a dictionnary with the bot's id and the bot's name

    def onHitWall(self):
        size = self.getMapSize()
        robotPosition = self.getPosition()
        angle = self.getHeading() % 360

        self.reset()  # To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event)
        if int(robotPosition.y()) > int(size.height())-100: #down
            self.turn(-(180-int(angle)))
            self.pause(30)
            if (270 < angle <= 360 or 0 <= angle < 90):
                self.move(-10)
            else:
                self.move(100)
        elif int(robotPosition.y()) < 100: #up
            self.turn(-(0 - int(angle)))
            self.pause(30)
            if 90 < angle < 270:
                self.move(-10)
            else:
                self.move(100)
        elif int(robotPosition.x()) > int(size.width())-100: #right
            self.turn(-(90 - int(angle)))
            self.pause(30)
            if 180 < angle < 360:
                self.move(-10)
            else:
                self.move(100)
        elif int(robotPosition.x()) < 100: #left
            self.turn(-(270 - int(angle)))
            self.pause(30)
            if 0 < angle < 180:
                self.move(-10)
            else:
                self.move(100)
        self.rPrint('ouch! a wall !')

    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower):  # NECESARY FOR THE GAME
        """ When i'm hit by a bullet"""
        self.reset()  # To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 
        self.rPrint("hit by " + str(bulletBotName) + "with power:" + str(bulletPower))

    def onBulletHit(self, botId, bulletId):  # NECESARY FOR THE GAME
        """when my bullet hit a bot"""
        self.rPrint("fire done on " + str(botId))

    def onBulletMiss(self, bulletId):  # NECESARY FOR THE GAME
        """when my bullet hit a wall"""
        self.rPrint("the bullet " + str(bulletId) + " fail")
        self.pause(10)  # wait 10 frames

    def onRobotDeath(self):  # NECESARY FOR THE GAME
        """When my bot die"""
        self.rPrint("damn I'm Dead")   
        
    #start_of_offense
    def onTargetSpotted(self, botId, botName, botPos):  # NECESARY FOR THE GAME
        "when the bot see another one"
        {onTargetSpotted_behaviour}
    #end_of_offense

'''
    with open(os.getcwd()+"\\Robots\\"+file_name, 'w') as file:
        file.write(class_template)

onTargetSpotted_behaviour_list = {
    'trackTarget' : f'''
        pos = self.getPosition()
        dx = botPos.x() - pos.x()
        dy = botPos.y() - pos.y()
        
        my_gun_angle = self.getGunHeading() % 360
        enemy_angle = math.degrees(math.atan2(dy, dx)) - 90
        a = enemy_angle - my_gun_angle
        if a < -180:
            a += 360
        elif 180 < a:
            a -= 360
        self.gunTurn(a)
        
        dist = math.sqrt(dx**2 + dy**2)
        if dist < FIRE_DISTANCE:
            self.fire(FIRE_POWER)
            
FIRE_DISTANCE = 500            
FIRE_POWER = {random.randint(1,10)}
''',
    'simple' : f'''
        self.fire(FIRE_POWER)
        self.rPrint("I see the bot:" + str(botId) + "on position: x:" + str(botPos.x()) + " , y:" + str(botPos.y()))
        
FIRE_POWER = {random.randint(1,10)}
''',
    'trackTarget_variablePower' : f'''
        pos = self.getPosition()
        dx = botPos.x() - pos.x()
        dy = botPos.y() - pos.y()

        my_gun_angle = self.getGunHeading() % 360
        enemy_angle = math.degrees(math.atan2(dy, dx)) - 90
        a = enemy_angle - my_gun_angle
        if a < -180:
            a += 360
        elif 180 < a:
            a -= 360
        self.gunTurn(a)

        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist < FIRE_DISTANCE:
            if dist <=80:
                setBulletPower(10)
            elif dist <=150:
                setBulletPower(7)
            elif dist <=200:
                setBulletPower(5)
            else:
                setBulletPower(2)

            self.fire(BULLET_POWER)
            setBulletPower(2)
            self.setRadarField("{random.choice(["normal", "large", "thin", "round"])}")
            
FIRE_DISTANCE = 500
def setBulletPower(power):
    global BULLET_POWER
    BULLET_POWER = power
'''
}

botCollision_behaviour_list = {
    'simple' : f'''
        self.rPrint('collision with:' + str(robotName))
''',
    'setRadarToRoud' : f'''
        self.setRadarField("round")
        self.rPrint('collision with:' + str(robotName))
'''
}

def generate_onTargetSpotted_behaviour():
    return onTargetSpotted_behaviour_list.get(random.choice(list(onTargetSpotted_behaviour_list.keys())))

def generate_botCollision_behaviour():
    return botCollision_behaviour_list.get(random.choice(list(botCollision_behaviour_list.keys())))



def generate_random_movement_behavior(radar_lock):
    movements = [
                    f'self.move({random.randint(movement_distance_min[1], movement_distance_max[1])})',
                    f'self.move({random.randint(movement_distance_max[0], movement_distance_min[0])})',
                    f'self.turn({random.randint(1, 180)})',
                    f'self.turn({random.randint(-180, -1)})',
                    f'self.gunTurn({random.randint(1, 180)})',
                    f'self.gunTurn({random.randint(-180, -1)})',
                    f'self.stop()',
                    f'self.radarTurn({random.randint(1, 180)})',
                    f'self.radarTurn({random.randint(-180, -1)})'
                ], [
                    f'self.move({random.randint(movement_distance_min[1], movement_distance_max[1])})',
                    f'self.move({random.randint(movement_distance_max[0], movement_distance_min[0])})',
                    f'self.turn({random.randint(1, 180)})',
                    f'self.turn({random.randint(-180, -1)})',
                    f'self.gunTurn({random.randint(1, 180)})',
                    f'self.gunTurn({random.randint(-180, -1)})',
                    f'self.stop()'
                ]

    if radar_lock == "free":
        movement_choice = movements[0]
    else:
        movement_choice = movements[1]
    setNUMBER_OF_STEPS()
    return [random.choice(movement_choice)for _ in range(NUMBER_OF_STEPS)]

def generateB(NUMBER_OF_BOTS):    
    classes_data = []

    for i in range(NUMBER_OF_BOTS):

        class_name = f'TrainingRobot{i + 1}'
        # movement_behaviour = [generate_random_movement_behavior() for _ in range(NUMBER_OF_STEPS)]
        radar_lock = random.choice(["gun", "free"])
        movement_behaviour = generate_random_movement_behavior(radar_lock)
        onTargetSpotted_behaviour = generate_onTargetSpotted_behaviour()
        botCollision_behaviour = generate_botCollision_behaviour()
        file_name = f'trainingRobot{i + 1}.py'

        class_info = {
            'class_name': class_name,
            'radar_lock': radar_lock,
            'movement_behaviour': movement_behaviour,
            'onTargetSpotted_behaviour': onTargetSpotted_behaviour,
            'botCollision_behaviour': botCollision_behaviour,
            'file_name': file_name
        }

        classes_data.append(class_info)


    for class_data in classes_data:
        generate_class_file(class_data['class_name'], class_data['radar_lock'], class_data['movement_behaviour'], class_data['onTargetSpotted_behaviour'],
                            class_data['botCollision_behaviour'], class_data['file_name'])
