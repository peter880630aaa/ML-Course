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
        pass

    def update(self, scene_info):
        """
        grid relative position
        |    |  10|    |
        |    |    |    |
        |    |  2 |    |
        |  1 |  5 |  3 |
        |  4 |  c |  6 |
        |  7 |  8 |  9 |
        |    |    |    |
        |    |    |    |       
        """
        def check_grid():
            grid = set()
            speed_ahead = 100
            speed_ahead_2 = 100
            dif_ahead = 250
            dif_coin = 1000
            side_coin = 0
            dif_left = 100
            dif_right = 100
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
                    if x <= 43 and x >= -43 :
                        if y > 0 and y < 280:
                            speed_ahead_2 = car["velocity"]
                            grid.add(10)
                            if y < 200:
                                grid.add(2)
                                if y < 140:
                                    if car["velocity"] < speed_ahead:
                                        speed_ahead = car["velocity"]
                                    if y < dif_ahead:
                                        dif_ahead = y
                                    grid.add(5) 
                        elif y < 0 and y > -105:
                            grid.add(8)
                    if x >= -70 and x < -43 :
                        if y > 80 and y < 120:
                            grid.add(3)
                        elif y < -80 and y > -105:
                            grid.add(9)
                        elif y < 80 and y > -80:
                            if (-x) < dif_right:
                                dif_right = (-x)
                            grid.add(6)
                    if x <= 70 and x > 43:
                        if y > 80 and y < 120:
                            grid.add(1)
                        elif y < -80 and y > -105:
                            grid.add(7)
                        elif y < 80 and y > -80:
                            if x < dif_left:
                                dif_left = x
                            grid.add(4)
            
            if scene_info.__contains__("coins"):
                for coin in scene_info["coins"]:
                    if coin[1] < self.car_pos[1]:
                        if self.car_pos[0] >= (coin[0] + 10 - 1) and self.car_pos[0] <= (coin[0] + 10 + 1):
                            dif_coin_p = 0
                            side_coin_p = 0
                        elif self.car_pos[0] > (coin[0] + 10):
                            dif_coin_p = self.car_pos[0] - (coin[0] + 10)
                            side_coin_p = 1
                        else:
                            dif_coin_p = (coin[0] + 10) - self.car_pos[0]
                            side_coin_p = 2
                        if dif_coin_p < dif_coin:
                            dif_coin = dif_coin_p
                            side_coin = side_coin_p

            return move(grid= grid, speed_ahead = speed_ahead, speed_ahead_2 = speed_ahead_2, dif_ahead= dif_ahead, side_coin = side_coin, dif_right = dif_right, dif_left = dif_left)
            
        def move(grid, speed_ahead, speed_ahead_2, dif_ahead, side_coin, dif_right, dif_left): 
            # if self.player_no == 0:
            #     print(grid)
            if (10 in grid) and (self.car_vel - speed_ahead_2) > 10:
                    if (9 not in grid) and (self.turn_left != 1):
                        return ["BRAKE", "MOVE_RIGHT"]
                    elif (7 not in grid):
                        self.turn_left = 1
                        return ["BRAKE", "MOVE_LEFT"]
                    else:
                        return ["BRAKE"]
            if dif_ahead < 85:
                if (9 not in grid) and (self.turn_left != 1):
                    return ["BRAKE", "MOVE_RIGHT"]
                elif (7 not in grid):
                    self.turn_left = 1
                    return ["BRAKE", "MOVE_LEFT"]
                else:
                    return ["BRAKE"]
            if dif_right <= 43:
                return ["SPEED", "MOVE_LEFT"]
            if dif_left <= 43:
                return ["SPEED", "MOVE_RIGHT"]
            if (1 not in grid) and (2 not in grid) and (3 not in grid) and (4 not in grid) and (5 not in grid) and (6 not in grid) and (7 not in grid) and (8 not in grid) and (9 not in grid):
                if side_coin == 0:
                    return ["SPEED"]
                elif side_coin == 1 and (self.car_pos[1] <= 540):
                    return ["SPEED", "MOVE_LEFT"]
                elif side_coin == 2 and (self.car_pos[1] <= 540):
                    return ["SPEED", "MOVE_RIGHT"]
                else:
                    return ["SPEED"]
            else:
                if (2 not in grid): # Check forward 
                    if self.turn_left == 1:
                        self.turn_left = 0
                    return ["SPEED"]
                else:
                    if (5 not in grid) and (self.turn_left == 1):
                        self.turn_left = 0
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
                        elif (6 not in grid) and (self.turn_left != 1): # turn right
                            if self.car_vel <= speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            elif (self.car_vel - speed_ahead) > 1:
                                return ["BRAKE", "MOVE_RIGHT"]
                            else:
                                return ["MOVE_RIGHT"]
                        elif (4 not in grid): # turn left
                            self.turn_left = 1
                            if self.car_vel <= speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            elif (self.car_vel - speed_ahead) > 1:
                                return ["BRAKE", "MOVE_LEFT"]
                            else:
                                return ["MOVE_LEFT"]
                        else : 
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]
                    #if (self.car_pos[0] < 60 ):
                        #return ["SPEED", "MOVE_RIGHT"]
                    elif (3 not in grid) and (6 not in grid) and (9 not in grid) and (self.turn_left != 1): # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    elif (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left
                        self.turn_left = 1
                        return ["SPEED", "MOVE_LEFT"]
                    elif (3 not in grid) and (6 not in grid) and (self.turn_left != 1): # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    elif (1 not in grid) and (4 not in grid): # turn left
                        self.turn_left = 1 
                        return ["SPEED", "MOVE_LEFT"]
                    elif (6 not in grid) and (9 not in grid) and (self.turn_left != 1): # turn right
                        return ["MOVE_RIGHT"]
                    elif (4 not in grid) and (7 not in grid): # turn left
                        self.turn_left = 1 
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
