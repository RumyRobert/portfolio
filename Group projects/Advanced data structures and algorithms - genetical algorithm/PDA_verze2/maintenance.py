import os
def returnedS(ret):
    #save results
    ret.sort()
    print("results: ",ret) #['32,Charlier', '35,Camper', '20,Demo', '31,generated']


    #filter non training bot names
    templist=[]
    temp2=[]
    for i in ret:
        if "TrainingRobot" in i:            
            templist.append(i)
        else:#save non training bots points
            temp2.append(i)

    print("BOT aquired ",templist[0].split(",")[0]," points") #['8,TrainingRobot1']

    
    with open(os.getcwd()+"\\results.txt","a") as file:
        for s in templist:
            file.write(str(s)+"\n")

    with open(os.getcwd()+"\\results1.txt","a") as file:
        for s in temp2:
            file.write(str(s)+"\n")
    
    