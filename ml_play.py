class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        self.check_side = 0
        self.turn_left = 0
        self.turn_right = 0
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        |    |  10|    |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        def check_grid():
            grid = set()
            speed_ahead = 100
            speed_ahead_2 = 100
            if self.car_pos[0] <= 35: # left bound
                grid.add(1)
                grid.add(4)
                grid.add(7)
                self.check_side = 1
            elif self.car_pos[0] >= 595: # right bound
                grid.add(3)
                grid.add(6)
                grid.add(9)
                self.check_side = 2
            
            if (self.check_side == 1) and (self.car_pos[0] > 75):
                self.check_side = 0
            elif (self.check_side == 2) and (self.car_pos[0] < 555):
                self.check_side = 0
            
            if self.check_side == 1:
                grid.add(1)
                grid.add(4)
                grid.add(7)
            elif self.check_side == 2:
                grid.add(3)
                grid.add(6)
                grid.add(9)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 40 and x >= -40 :
                        if y > 0 and y < 320:
                            speed_ahead_2 = car["velocity"]
                            grid.add(10)
                            if y < 270:
                                grid.add(2)
                                if y < 140:
                                    speed_ahead = car["velocity"]
                                    grid.add(5) 
                        elif y < 0 and y > -105:
                            grid.add(8)
                    if x >= -70 and x < -40 :
                        if y > 80 and y < 120:
                            grid.add(3)
                        elif y < -80 and y > -105:
                            grid.add(9)
                        elif y < 80 and y > -80:
                            grid.add(6)
                    if x <= 70 and x > 40:
                        if y > 80 and y < 120:
                            grid.add(1)
                        elif y < -80 and y > -105:
                            grid.add(7)
                        elif y < 80 and y > -80:
                            grid.add(4)
            return move(grid= grid, speed_ahead = speed_ahead, speed_ahead_2 = speed_ahead_2)
            
        def move(grid, speed_ahead, speed_ahead_2): 
            # if self.player_no == 0:
            #     print(grid)
            if len(grid) == 0:
                if self.car_pos[0] > self.lanes[self.car_lane]:
                    return ["SPEED", "MOVE_LEFT"]
                elif self.car_pos[0] < self.lanes[self.car_lane]:
                    return ["SPEED", "MOVE_RIGHT"]
                else :return ["SPEED"]
            else:
                if (10 in grid) and (self.car_vel - speed_ahead_2) > 7:
                    if (7 not in grid):
                        return ["BRAKE", "MOVE_LEFT"]
                    elif (9 not in grid):
                        return ["BRAKE", "MOVE_RIGHT"]
                    else:
                        return ["BRAKE"]
                if (2 not in grid): # Check forward 
                    # Back to lane center
                    if self.car_pos[0] > self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0] < self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_RIGHT"]
                    else :return ["SPEED"]
                else:
                    if (5 not in grid) and (self.turn_left == 1):
                        self.turn_left = 0
                    if (5 not in grid) and (self.turn_right == 1):
                        self.turn_right = 0
                    if (5 in grid): # NEED to BRAKE
                        if (3 not in grid) and (6 not in grid) and (self.turn_left != 1):
                            if self.car_vel <= speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            elif (self.car_vel - speed_ahead) > 1:
                                return ["BRAKE", "MOVE_RIGHT"]
                            else:
                                return ["MOVE_RIGHT"]
                        elif (1 not in grid) and (4 not in grid):
                            self.turn_left = 1
                            if self.car_vel <= speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            elif (self.car_vel - speed_ahead) > 1:
                                return ["BRAKE", "MOVE_LEFT"]
                            else:
                                return ["MOVE_LEFT"]
                        elif (4 not in grid) and (self.turn_right != 1): # turn left 
                            if self.car_vel <= speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            elif (self.car_vel - speed_ahead) > 1:
                                return ["BRAKE", "MOVE_LEFT"]
                            else:
                                return ["MOVE_LEFT"]
                        elif (6 not in grid): # turn right
                            self.turn_right = 1
                            if self.car_vel <= speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            elif (self.car_vel - speed_ahead) > 1:
                                return ["BRAKE", "MOVE_RIGHT"]
                            else:
                                return ["MOVE_RIGHT"]
                        else : 
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]
                    #if (self.car_pos[0] < 60 ):
                        #return ["SPEED", "MOVE_RIGHT"]
                    elif (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    elif (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    elif (1 not in grid) and (4 not in grid): # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    elif (3 not in grid) and (6 not in grid): # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    elif (6 not in grid) and (9 not in grid): # turn right
                        return ["MOVE_RIGHT"]
                    elif (4 not in grid) and (7 not in grid): # turn left 
                        return ["MOVE_LEFT"]
                                
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass
