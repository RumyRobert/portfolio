import os
import random
global directory,bots
directory =os.getcwd()+"\\Robots" #'.'  # Change this to the path of your directory 

files = os.listdir(directory)

combined_bots = []
bots = [] 




def copyRadar(input):
    movement_lines = []
    try:
        #print(directory+"\\"+input)
        with open(directory+"\\"+input, 'r') as input_file:
            inside_block = False
            for line in input_file:
                if "#start_of_radar" in line or inside_block:
                    inside_block = True
                    movement_lines.append(line)
                if "#end_of_radar" in line:
                    inside_block = False
        input_file.close()
    except FileNotFoundError:
        print(f"File not found: {input} copyRadar")
    except Exception as e:
        print(f"An error occurred: {e}")
    return movement_lines

def copyMovement(input):
    movement_lines = []
    try:
        with open(directory+"\\"+input, 'r') as input_file:
            inside_block = False
            for line in input_file:
                if "#start_of_movement" in line or inside_block:
                    inside_block = True
                    movement_lines.append(line)
                if "#end_of_movement" in line:
                    inside_block = False
        input_file.close()
    except FileNotFoundError:
        print(f"File not found: {input} copyMovement")
    except Exception as e:
        print(f"An error occurred: {e}")
    return movement_lines

def copyOffense(input):
    offense_lines = []
    try:
        with open(directory+"\\"+input, 'r') as input_file:
            inside_block = False
            for line in input_file:
                if "start_of_offense" in line or inside_block:
                    inside_block = True
                    offense_lines.append(line)
                if "#end_of_offense" in line:
                    inside_block = False
        input_file.close()
    except FileNotFoundError:
        print(f"File not found: {input} copyOffense")
    except Exception as e:
        print(f"An error occurred: {e}")
    return offense_lines

def copyCollision(input):
    offense_lines = []
    try:
        with open(directory+"\\"+input, 'r') as input_file:
            inside_block = False
            for line in input_file:
                if "start_of_collision" in line or inside_block:
                    inside_block = True
                    offense_lines.append(line)
                if "#end_of_collision" in line:
                    inside_block = False
        input_file.close()
    except FileNotFoundError:
        print(f"File not found: {input} copyCollision")
    except Exception as e:
        print(f"An error occurred: {e}")
    return offense_lines


def findHighestNumber(temp_bots):
    numbers = []
    for bot in temp_bots:
        if "trainingRobot" in bot:
            number = [int(bot.split("trainingRobot")[1].split(".")[0])]
            numbers.append(number)
    highest = max(numbers) if numbers else None
    return highest[0]

def combination(robot1, robot2):
    print("Combine: ",robot1," and ", robot2)
    for file in files: #musí zůstat pro highestnumber
        if "trainingRobot" in file:
            file_name = os.path.basename(file)
            bots.append(file_name)

    # # Find the highest number
    temp_bots = bots
    highest_number = findHighestNumber(temp_bots)

    # Create a new file with the next number
    next_number = highest_number + 1
    new_file_name = f'trainingRobot{next_number}.py'

    parents = [robot1, robot2]
    random_numbers = [random.randint(0, 1) for _ in range(4)]

    # Check if all numbers are the same and regenerate if needed
    while all(num == random_numbers[0] for num in random_numbers):
        random_numbers = [random.randint(0, 1) for _ in range(4)]

    movements = copyMovement(parents[random_numbers[0]])
    movement_settings = []
    for mov_line in movements:
        movement_settings.append(mov_line)
    movements = "\n".join(movement_settings)


    offense = copyOffense(parents[random_numbers[1]])
    offense_settings = []
    for off_line in offense:
        offense_settings.append(off_line)
    offense = "\n".join(offense_settings)


    collision = copyCollision(parents[random_numbers[2]])
    collision_settings = []
    for col_line in collision:
        collision_settings.append(col_line)
    collision = "\n".join(collision_settings)


    radar = copyRadar(parents[random_numbers[3]])
    radar_settings = []
    for rad_line in radar:
        radar_settings.append(rad_line)
    radar = "\n".join(radar_settings)


    cosmetics = f'''
#! /usr/bin/python
# -*- coding: utf-8 -*-

import math

#combination of: '{robot1}'' {robot2}'

from robot import Robot  # Import a base Robot

class TrainingRobot{next_number}(Robot):  # Create a Robot

    def init(self):  # NECESSARY FOR THE GAME   To initialize your robot

        # Set the bot color in RGB
        self.setColor(0, 200, 100)
        self.setGunColor(200, 200, 0)
        self.setRadarColor(255, 60, 0)
        self.setBulletsColor(0, 200, 100)

        # get the map size
        size = self.getMapSize()  # get the map size
        self.radarVisible(True)  # show the radarField')
        
        {radar}
        
        {movements}
        
        {collision}
        
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
        
        {offense}

'''
    with open(os.getcwd()+"\\Robots\\"+new_file_name, 'w') as new_file:  # You can write content to the new file if needed
        new_file.write(cosmetics)


        # new_file.write('\n')
        # for mov_line in movements:
        #     new_file.write(mov_line)
        # new_file.write('\n')
        # for col_line in collision:
        #     new_file.write(col_line)
        # new_file.write('\n')
        # for off_line in offense:
        #     new_file.write(off_line)
        # new_file.write('\n')
    print(f"New file '{new_file_name}' created")
    new_file.close()
    temp_bots.append(new_file_name)
    return new_file_name


#for i in range(0, (int(len(bots)/2))*2, 2):
#    print(i)
#    if bots[i+1] is not None:
#        combination(bots[i], bots[i+1])

