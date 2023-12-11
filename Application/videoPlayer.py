import moviepy
from moviepy.editor import *
import pygame



def playVideo(path):
    pygame.init()
    clip = VideoFileClip(path).resize(1.0)
    clip.preview()
    pygame.display.quit()
