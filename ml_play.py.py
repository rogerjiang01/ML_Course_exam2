"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from mlgame.communication import ml as comm

'''def ml_loop_for_1P(plat, point):
    if (plat[0]+20 > point):
        comm.send_to_game({"frame": scene_info["frame"], "command_1P": "MOVE_LEFT"})
    elif (plat[0]+20 < point):
        comm.send_to_game({"frame": scene_info["frame"], "command_1P": "MOVE_RIGHT"})
    else:
        comm.send_to_game({"frame": scene_info["frame"], "command_1P": "NONE"})'''

#def ml_loop_for_2P():


def point1_down(point):
    if (point > 200):
        if (int(point / 200) == 1):
            point = 400-point #-(200-cur[0])
        elif (int(point / 200) == 2):
            point = point-400 #-(200-cur[0])
        elif (int(point / 200) == 3):
            point = 800-point #-(200-cur[0])
    elif (point < 0):
        if (int(point / 200) == 0):
            point = -point #+cur[0]
        elif (int(point / 200) == -1):
            point = 400+point #+cur[0]
        elif (int(point / 200) == -2):
            point = 400-point #+cur[0]
    return point

def point1_up(cur, m):
    point1cx = (cur[0]-(cur[1]-260)/m)
    if (point1cx > 200):
        if (int(point1cx/200) == 1):
            point1cx = 400 - point1cx
        elif (int(point1cx/200) == 2):
            point1cx = point1cx - 400
            m = -m
        elif (int(point1cx/200) == 3):
            point1cx = 800 - point1cx
    elif (point1cx < 0):
        if (int(point1cx/200) == 0):
            point1cx = -point1cx
        elif (int(point1cx/200) == -1):
            point1cx = 400 + point1cx 
            m = -m
        elif (int(point1cx/200) == -2):
            point1cx = 400 - point1cx
    else:   
        m = -m

    point1 = (point1cx + (160/m))
    return point1_down(point1)



def ml_loop(side: str):
    """
    The main loop for the machine learning process

    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```

    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information
        
        cur=[0,0] # a,b
        cur = list(scene_info["ball"])
        vel = list(scene_info["ball_speed"])
        plat1 = list(scene_info["platform_1P"])
        plat2 = list(scene_info["platform_2P"])
        #block = list(scene_info["blocker"])

        if (vel[0] == 0):
            m = 1
        else: 
            m = vel[1]/vel[0] #斜率(vy/vx)
            
        point1 = cur[0] + ((420-cur[1])/m) #1P的落點
        point2 = cur[0] - ((cur[1]-80)/m)  #2P的落點
        #point1c = [100,260]
        #point2c = [100,240]

        #print(cur)
        #print(vel)

        if (vel[1]>0 and cur[1]>110):
            point1 = point1_down(point1)
        elif(vel[1]<0 and cur[1]>260):
            point1 = point1_up(cur, m)
        elif(vel[1]<0 and cur[1]<260):
            point1 = 100

        print(point1)
        
        #ml_loop_for_1P(plat1, point1)

        # 3.4 Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
        else:
            #comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            if (vel[1] == 0):
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            else:
                if (plat1[0]+20 > point1):
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
                elif (plat1[0]+20 < point1):
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
                else:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
