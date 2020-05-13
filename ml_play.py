"""
The template of the main script of the machine learning process
"""
import pickle
from os import path

import numpy as np
from mlgame.communication import ml as comm


def ml_loop(side: str):
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False
    filename = path.join(path.dirname(__file__), 'save', 'clf_Knn_BallAndDirection_1P_2.pickle')
    with open(filename, 'rb') as file:
        clf = pickle.load(file)
    

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()
    


    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.recv_from_game()
        feature = []
        feature.append(scene_info["ball"][0])
        feature.append(scene_info["ball"][1])
        feature.append(scene_info["ball_speed"][0])
        feature.append(scene_info["ball_speed"][1])
        #feature.append(scene_info["blocker"][0])

        feature = np.array(feature)
        feature = feature.reshape((-1,4))
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
        else:
                
            x = clf.predict(feature)
            x2 = scene_info["platform_1P"][0]
            
            if x == -1 and x2 <= 85 and x2 >= 75:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif x == -1 and x2 < 80:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            elif x == -1 and x2 > 80:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            #elif (x2 + 20) <= (x + 5) and (x2 + 20) >= (x - 5):
                #comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif x == (x2 + 20):
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
                #print('NONE')
            elif x > (x2 + 20):
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
                #print('LEFT')
            elif x < (x2 + 20):
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
                #print('RIGHT')
