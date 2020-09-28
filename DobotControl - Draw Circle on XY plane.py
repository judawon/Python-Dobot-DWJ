import threading #병렬 처리
import DobotDllType as dType
import math

# Condition String
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll and get the CDLL object
api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):
    
    # Clean Command Queued
    dType.SetQueuedCmdClear(api) 

    # Async Motion Params Setting
    dType.SetHOMEParams(api, 200, 110, 65, 50,isQueued = 1)
    

    # 속도 
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)

    #Async Home
    dType.SetHOMECmd(api, temp = 0, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
   
    #Draw Circle :
    #dType.SetCircleCmd(api, 200,200,100,200, isQueued = 1)

    steps = 24
    scale = 50
    for i in range(steps + 2):
        x = math.cos(((math.pi * 2) / steps ) * i)
        y = math.sin(((math.pi * 2) / steps ) * i)        
        lastIndex = dType.SetPTPCmd(api,dType.PTPMode.PTPMOVLXYZMode, 200+x*scale,110+y*scale,65,50, isQueued = 1)[0] 
    
    #Start to Execute Command Queue
    dType.SetQueuedCmdStartExec(api)

    #Wait for Executing Last Command 
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)

    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)

#Disconnect Dobot
dType.DisconnectDobot(api)

    
    
