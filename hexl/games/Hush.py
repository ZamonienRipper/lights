import numpy as np
import collections
from collections import deque
import itertools
import time
import queue

class Hush:
    def __init__(self):
        self.colorful = False
        self.points = 0
        self.suits = 2
        self.game_points = 3
        self.gaming = True
        self.fields = [0,1,2,3,4,5,6,7,8,9,10,11,12]
        self.grid = {12:0, 0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0}
        self.colors = [(0,0,0), (0,255,0), (0,0,255), (255,0,255)]
        self.inner = deque([2,1,0,5,4,3], maxlen=6)
        self.randomization_times = [.5,.5,.4,.4,.3,.3,.2,.2,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.3,.5]
        #self.randomization_times = [.1,.1]
        self.single_player = deque([1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.two_player = deque([1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.three_player = deque([1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.player_indicators = [self.single_player, self.two_player, self.three_player]
        self.player_seq = [deque([1]), deque([1,2]), deque([1, 2, 3])]
        self.players = 1

    def nxt(self, field):
        if self.inner.index(field) in [0,5]:
            self.inner.rotate(2)
        return self.inner[self.inner.index(field)+1]
    
    def prv(self, field):
        if self.inner.index(field) in [0,5]:
            self.inner.rotate(2)
        return self.inner[self.inner.index(field)-1]
    def out(self, field):
        return field + 6
    def inn(self, field):
        return field - 6
    
        
    def randomize_grid(self, LightController):
        prev = 3
        for key in self.grid:
            if prev == 1:
                self.grid[key] = 2
                prev = 2
            elif prev == 2:
                self.grid[key] = 3
                prev = 3
            elif prev == 3:
                self.grid[key] = 1
                prev = 1
        for round, delay in enumerate(self.randomization_times):
            self.rotate_grid(np.random.choice(self.inner),np.random.choice([True, False]))
            self.update_light(LightController)
            time.sleep(delay)
        while self.checkGrid() is not None:
            self.rotate_grid(np.random.choice(self.inner),np.random.choice([True, False]))
            time.sleep(0.1)
        

    def rotate_grid(self, direction, clockwise):
        next = self.grid.copy()
        active = deque([99, 99, 99, 99], maxlen=4)
        active[0] = 12
        active[2] = direction + 6
        if clockwise:
            active[1] = self.prv(direction)
            active[3] = self.nxt(direction)
        else:
            active[1] = self.nxt(direction)
            active[3] = self.prv(direction)

        for elem in [0,0,0,0]:
            next[active[elem]] = self.grid[active[elem-1]]
            active.rotate(1)
        self.grid = next

    def update_light(self, LightController):
        pixels = []
        colors = []
        for i, key in enumerate(self.grid.keys()):
            pixels.append(key)
            colors.append(self.colors[self.grid[key]])
        LightController.pixelsChange(pixels, colors)

    def getInput(self, gameFreq, LightController, eventPile):
        colorWheel = ((0,255,0), (127,255,0), (255,255,0), (255,127,0), (255,0,0))
        player_indicator = self.player_indicators[self.player_seq[0]-1].copy()
        eventPile.clear()
        wait = 1
        while wait:
            if eventPile:
                direction = np.where(eventPile.popleft() == 1)[0][0]
                print(f'Chosen direction: {direction}')
                eventPile.clear()
                LightController.pixelChange(direction, (255,255,255))
                time.sleep(0.4)
                while wait:
                    LightController.pixelsChange([self.out(self.nxt(direction)), self.out(self.prv(direction))], [(255,255,255), (255,255,255)])
                    indicator = player_indicator[0]
                    LightController.pixelChange(direction, (indicator*255,indicator*255,indicator*255))
                    player_indicator.rotate(-1)
                    if eventPile:
                        clockwise = np.where(eventPile.popleft() == 1)[0][0]
                        print(f'Chosen clockwise: {clockwise}')
                        if clockwise == direction:
                            self.update_light(LightController)
                            eventPile.clear()
                            break
                        elif clockwise not in [self.nxt(direction), self.prv(direction)]:
                            LightController.pixelsChange([self.out(self.nxt(direction)), self.out(self.prv(direction))], [(255,0,0), (255,0,0)])
                            time.sleep(0.4)
                            LightController.pixelsChange([self.out(self.nxt(direction)), self.out(self.prv(direction))], [(255,255,255), (255,255,255)])
                            eventPile.clear()
                        elif self.prv(clockwise) == direction:
                            self.update_light(LightController)
                            return (direction, True)
                        else:
                            self.update_light(LightController)
                            return (direction, False)
                    time.sleep(gameFreq)
            time.sleep(gameFreq)
            
        LightController.pixelOff(self.INDICATOR_LED)
        return self.INPUT_CHANNELS

    def checkGrid(self):
        mid = self.grid[12]
        print(f'Winning color: {mid}')
        if mid > 0:
            length = np.zeros(6)
            for direction in range(3):
                winners = [12, ]
                if self.grid[direction] == mid:
                    winners.append(direction)
                    length[direction] += 1
                    if self.grid[self.out(direction)] == mid:
                        winners.append(self.out(direction))
                        length[direction] += 1
                if self.grid[direction + 3] ==mid:
                    winners.append(direction + 3)
                    if self.grid[self.out(direction + 3)] == mid:
                        winners.append(self.out(direction + 3))
                if len(winners) > 3:
                    print(f'Winning grid fields: {winners}')
                    return winners
        print('No winners found this move')
        return None
            
    def removeWinner(self, winners, LightController):
        winning_color = self.grid[12]
        for winner in winners:
            self.grid[winner] = 0
        print(f'{winners=}')
        for i in range(3):
            LightController.pixelsChange(winners, [self.colors[winning_color] for x in winners])
            time.sleep(1)
            LightController.pixelsChange(winners, [(0,0,0) for x in winners])
            time.sleep(.5)

    def selectMode(self, LightController, eventPile):
        player_selectors = {1:7, 2:8, 3:9}
        
        lights_sequence = deque([7, 0, 8, 8, 0, 9, 9, 9, 0])
        
        while 1:
            if lights_sequence[0] != 0:
                LightController.pixelChange(lights_sequence[0], (255,255,255))
                time.sleep(0.2)
                LightController.pixelChange(lights_sequence[0], (0,0,0))
                time.sleep(0.2)
            else:
                time.sleep(0.2)
            lights_sequence.rotate(-1)
            if eventPile:
                players = np.where(eventPile.popleft() == 1)[0][0]
                eventPile.clear()
                if players in player_selectors.keys():
                    for i in range(players):
                        LightController.pixelChange(12, (255,255,255))
                        time.sleep(0.3) 
                        LightController.pixelChange(12, (0,0,0))
                        time.sleep(0.3) 
                    self.players = players
                    self.player_seq = self.player_seq[players-1]
                    self.score = np.zeros(players)
                    print(f'Player selection done: {self.players}')
                    break
                else:
                    continue

    def showScore(self, gameFreq, LightController, eventPile):
        player_one_seq = deque([1, 1, 1, 0, 0, 1, 1, 1])
        player_two_seq = deque([1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1])
        player_three_seq = deque([1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1])
        player_seqs = [player_one_seq, player_two_seq, player_three_seq]
        eventPile.clear()
        game_over = 0
        score_pixels = [0, 2, 4]
        score_colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
        winning_score = max(self.score)
        for player, score in enumerate(self.score):
            if score == winning_score:
                score_colors[player] = (0,255,0)
            else:
                score_colors[player] = (255,255,255)
        time.sleep(0.4)
        print(f'{self.score=}')
        print(f'{score_colors=}')
        while 1:
            for i in range(self.players):
                for j in range(8+6*i):
                    LightController.pixelChange(score_pixels[i], tuple(k*player_seqs[i][0] for k in score_colors[i]))
                    player_seqs[i].rotate(-1)
                    time.sleep(gameFreq)
                    if eventPile:
                        print('GAME OVER')
                        print(f'{eventPile=}')
                        LightController.offWipeFast(50)
                        game_over = 1
                        break
                if game_over:
                    break
            if game_over:
                break
        
    def play(self, gameFreq, LightController, eventPile):
        self.selectMode(LightController, eventPile)
        self.randomize_grid(LightController)
        while sum(self.score) < self.game_points:
            
            (dir, clockwise) = self.getInput(gameFreq, LightController, eventPile)
            self.rotate_grid(dir, clockwise)
            self.update_light(LightController)
            self.player_seq.rotate(-1)
            winner = self.checkGrid()
            print(winner)
            if winner != None:
                self.score[self.player_seq[0]-1] += 1
                self.removeWinner(winner, LightController)                   
            self.update_light(LightController)
        LightController.offWipeFast(50)
        self.score = [1, 0, 1]
        if self.players > 1:
            self.showScore(gameFreq, LightController, eventPile)
        print('GAME OVER')
        

