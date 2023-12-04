import moviepy
from moviepy.editor import *
import pygame



def playVideo(path):
    clip = VideoFileClip(path)
    clip.preview().resize(1.5)
    pygame.quit()

# playVideo('Assets\\Video\\baby.mp4')