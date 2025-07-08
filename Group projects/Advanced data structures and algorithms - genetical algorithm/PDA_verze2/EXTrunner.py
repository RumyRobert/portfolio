
from ctypes.wintypes import POINT
import main
import os,sys
import subprocess
from window import setEXT
import PopulationInitialization4
import Combine

def runner():
    print("1=normální; 2=učení; 3=tanky")
    #a=int(input())
    a=2
    if a==1:
        print("vybráno: normální")
    elif a==2:
        print("vybráno: učení")
        main.setextRUN()
        setEXT()
        

    elif a==3:
        print("Creating bots") 
        NUMBER_OF_BOTS = 100      #Number of Robots to be generated        
        PopulationInitialization4.generateB(NUMBER_OF_BOTS)

    elif a==4:
        Combine.combination("trainingRobot1.py", "trainingRobot2.py")
        os._exit(1)

    else:
        print("wrong selection")
        os._exit(1)
  
runner() # menu

listGEN=["trainingRobot1"]
listORG=["coin","demo","generated","charlier","T800","track_target","wall_runner","wall_tt"]




#generate listGEN from folder for first run
def genList():
    trainingbotList=[]
    botFiles11 = os.listdir(os.getcwd() + "/Robots")
    
    for bot in botFiles11:
        if "trainingRobot" in bot:
            trainingbotList.append(bot[:-3])
    return trainingbotList



#test each bot individually
def testBot(trainingbotList):
    for bt in trainingbotList:
        try:
            main.RUN(listORG,[bt])            

        except:
            pass

def loadPoints(filename):
    with open(os.getcwd()+filename,"r") as file:
        lines=[]
        for line in file:
            line=line.strip()
            lines.append(line)
    #print("LOADED ",lines)
    file.close()

    return lines


bestFOund=True
learnCount=0
while bestFOund:    
    learnCount+=1
    if learnCount < 2: #get points from all bots in folder
        #continue
        PopulationInitialization4.generateB(25)
        testBot(genList()) 
    
    #Load bots order
    points1=loadPoints("\\results.txt")  #["53,bot1","55,bot2"]
    points=sorted(points1,key=lambda x: float(x.split(",")[0]),reverse=True)
    

    #select few best bots
    Botcount=len(points)
    if Botcount % 2!=0:
        Botcount-=1
    

    #combine them   
    newBots=[]
    for RNG in range(Botcount//2):
        print("trainingRobot"+str(RNG+1)+".py")
        newBot=Combine.combination("trainingRobot"+str(RNG+1)+".py", "trainingRobot"+str(RNG+2)+".py")
        print("TEST ",newBot)
        newBots.append(newBot[:-3])

    #evaluate combined bots
    print("New Bots ",newBots)
    testBot(newBots) 

    #Load bots order again
    points1=loadPoints("\\results.txt")  #["53,bot1","55,bot2"]
    points=sorted(points1,key=lambda x: float(x.split(",")[0]),reverse=True)
    print("Actual score",points)
    
    

    #Load defalut bots order
    points2=loadPoints("\\results1.txt")  #["53,bot1","55,bot2"]
    points3=sorted(points2,key=lambda x: float(x.split(",")[0]),reverse=True)
    print("\nBest score so far: ",points[0])
    print("\nBest points default",points3[0])
    print("\nwaiting, pres enter to continue")
    input()

    #Check if best bot has been found. If not, continue.   
    
    #NTpoint=56
    NTpoint=int(points3[0].split(",")[0])
    if NTpoint <= int(points[0].split(",")[0]):
        print("Best bot has been found")
        print("\nBest bot: ",points[0])
        bestFOund=False
    else:
        print("Default bot is still better, continue with next step")
        #PopulationInitialization4.generateB(100)
        
    
    #prevent while loop deadlock
    if learnCount >1000000:
        print("prevented while loop")
        sys.exit(0)

    """
    templist=[]
    for i in ret:
        if "TrainingRobot" in i:            
            templist.append(i)
    """

print("END")







