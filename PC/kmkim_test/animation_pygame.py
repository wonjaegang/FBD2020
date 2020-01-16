import pygame
import sys
import time

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SIZE = 20

white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()
pygame.display.set_caption("Pygame Test")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#clock = pygame.time.Clock()
pos_x = 200
pos_y = 480
while True:
	y=int(input("입력: "))
	screen.fill(black)
	pygame.display.update()
	while y != pos_y:
		#clock.tick(10)
		if y < pos_y:
			pos_y -= 5
		elif y > pos_y:
			pos_y += 5
		screen.fill(black)
		pygame.draw.rect(screen, white, [pos_x, pos_y, 2 * SIZE, 4 * SIZE], 10)
		pygame.display.update()
		time.sleep(0.1)