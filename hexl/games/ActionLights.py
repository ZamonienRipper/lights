import time
import numpy as np

class ActionLights:
    def __init__(self):
        self.INPUT_CHANNELS = 6
        self.COOLDOWN = 15
        self.previousState = np.zeros(self.INPUT_CHANNELS, dtype=np.int8)
        self.countdown = np.zeros(self.INPUT_CHANNELS, dtype=np.uint8)
        
    def play(self, gameFreq, LightController, eventPile):
        def decrement(array):
            result = np.array(np.sqrt((array-1)*array),dtype=np.uint8)
            return result
        
        #print('ENTERING GAME')
        while True:
            time.sleep(gameFreq)
            #print('RUNNING ANOTHER ROUND OF THE GAME')
            #print(f"eventpile length inside play: {len(eventPile)}")
            if len(eventPile) > 0:
                #print(f"eventPile inside play: {eventPile}")
                newEvent = eventPile.popleft()
                changes = np.where(newEvent == 1)[0]
                for channel in changes:
                    self.countdown[channel] = self.COOLDOWN
            for channel, state in enumerate(self.countdown):
                if state > 0:
                    if state == 15:
                        LightController.pixelChange(channel, (255, 0, 0))
                    elif state == 10:
                        LightController.pixelChange(channel, (255, 100, 0))
                    elif state == 6:
                        LightController.pixelChange(channel, (150, 200, 0))
                    elif state == 1:
                        LightController.pixelOff(channel)
            self.countdown = decrement(self.countdown)