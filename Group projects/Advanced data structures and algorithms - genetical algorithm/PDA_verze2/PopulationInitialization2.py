import random
import os
NUMBER_OF_BOTS = 4      #Number of Robots to be generated
NUMBER_OF_STEPS = 15    #Number of how many steps each Robot will have


def generate_class_file(class_name, movement_behaviour, fire_power, file_name):
    movement_code = '\n        '.join(movement_behaviour)

    class_template = f'''
#! /usr/bin/python
# -*- coding: utf-8 -*-

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

    def run(self):  # NECESARY FOR THE GAME  main loop to command the bot

        {movement_code}

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

    def onHitByRobot(self, robotId, robotName):
        self.rPrint("damn a bot collided me!")

    def onHitWall(self):
        self.reset()  # To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 
        self.pause(100)
        self.move(-100)
        self.rPrint('ouch! a wall !')
        self.setRadarField("large")  # Change the radar field form

    def onRobotHit(self, robotId, robotName):  # when My bot hit another
        self.rPrint('collision with:' + str(
            robotName))  # Print information in the robotMenu (click on the righ panel to see it)

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

    def onTargetSpotted(self, botId, botName, botPos):  # NECESARY FOR THE GAME
        "when the bot see another one"
        self.fire({fire_power})
        self.rPrint("I see the bot:" + str(botId) + "on position: x:" + str(botPos.x()) + " , y:" + str(botPos.y()))


'''

    with open(os.getcwd()+"\\Robots\\"+file_name, 'w') as file:
        file.write(class_template)

def generate_random_movement_behavior():
    movements = [
        f'self.move({random.randint(10, 100)})',
        f'self.move({random.randint(-100, -10)})',
        f'self.turn({random.randint(1, 180)})',
        f'self.turn({random.randint(-180, -1)})',
        f'self.fire({random.randint(1, 10)})',
        f'self.gunTurn({random.randint(1, 180)})',
        f'self.gunTurn({random.randint(-180, -1)})',
        f'self.stop()',
        f'self.radarTurn({random.randint(1, 180)})',
        f'self.radarTurn({random.randint(-180, -1)})'
    ]
    return random.choice(movements)


def generateB(NUMBER_OF_BOTS,NUMBER_OF_STEPS):
    classes_data = []

    for i in range(NUMBER_OF_BOTS):

        class_name = f'TrainingRobot{i + 1}'
        movement_behaviour = [generate_random_movement_behavior() for _ in range(NUMBER_OF_STEPS)]
        fire_power = random.randint(1, 10)        
        file_name = f'trainingRobot{i + 1}.py'

        class_info = {
            'class_name': class_name,
            'movement_behaviour': movement_behaviour,
            'fire_power': fire_power,
            'file_name': file_name
        }

        classes_data.append(class_info)


    for class_data in classes_data:
        generate_class_file(class_data['class_name'], class_data['movement_behaviour'], class_data['fire_power'], class_data['file_name'])


#NUMBER_OF_BOTS = 4      #Number of Robots to be generated
#NUMBER_OF_STEPS = 15    #Number of how many steps each Robot will have
#generateB(NUMBER_OF_BOTS,NUMBER_OF_STEPS)