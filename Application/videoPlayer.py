import moviepy
from moviepy.editor import *
import pygame



def playVideo(path):
    clip = VideoFileClip(path).resize(1.5)
    clip.preview()
    pygame.quit()

# playVideo('Application\\Assets\\Video\\baby.mp4')