import alsaaudio
import audioop
import pygame
import recursive_art as ra
import numpy as np
import sys
   

class Visualizer(object):
    """An audio visualizer that computationally generates frames of an animation,
    then chooses a frame to display based on the volume read from the mic.

    Attributes:
    generate: If True, generates a new set of frames (this takes a while)
    w, h: The width and height of the images generated
    filename: The filename of the images generated (include a % formatting flag)
    image_count: the number of frames generated"""

    def __init__(self, generate = False, w = 640, h = 480, filename = "frame%03d.png", image_count = 100):
        self.w = w
        self.h = h
        self.filename = filename
        self.image_count = image_count

        if generate:
            print "Generating images..."
            ra.generate_art(filename,w,h,image_count)

    def visualize(self):
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,0)
        inp.setchannels(1)
        inp.setrate(16000)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        #Runs at about ~50 fps
        inp.setperiodsize(320)

        min_vol, max_vol = np.sqrt(10), np.sqrt(24000)
               
        images = {}

        print "Loading images..."
        #Load all the images beforehand, so they don't need to be loaded
        #Individually in real time
        for i in range(self.image_count):
            images[i] = pygame.image.load(self.filename%i)

        print "Visualizing!"
        pygame.init()
        size=(self.w,self.h)
        screen = pygame.display.set_mode(size)

        while True:
                l,data = inp.read()
                vol = np.sqrt(audioop.rms(data,2))

                if vol < min_vol:
                    min_vol = vol
                elif vol > max_vol:
                    max_vol = vol

                image_index = ra.remap_interval(vol,
                    min_vol,max_vol,
                    0,self.image_count-1)

                image_index = int(image_index)

                screen.blit(images[image_index],(0,0))
                pygame.display.flip()

if __name__ == "__main__":
    if sys.argv[1] == "generate":
        vis = Visualizer(True)
    else:
        vis = Visualizer(False)

    vis.visualize()
