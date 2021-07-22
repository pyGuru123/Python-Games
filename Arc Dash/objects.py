import pygame
import random
import math

SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

pygame.font.init()
pygame.mixer.init()


def draw_arc(win, rect, theta1, theta2):
	pygame.draw.arc(win, (0,0,0), rect, theta1, theta2, 10)
