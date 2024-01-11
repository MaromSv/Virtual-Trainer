from multiprocessing import Process
import pygame
import time
import threading


def play_background_music(volume=0.5):
    pygame.mixer.init()
    pygame.mixer.music.load('Application\\Assets\\Audio\\li-jali-cucu-8466.mp3')
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely


my_thread = threading.Thread(target=play_background_music, name="MyThread")
my_thread.start()
time.sleep(30) # Sleep for 3 seconds

my_thread.join()