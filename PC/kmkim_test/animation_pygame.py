import pygame
import sys
import time

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 600
SIZE = 100

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

pygame.init()
pygame.display.set_caption("Pygame Test")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font('freesansbold.ttf',30)
text_B1 = font.render("B1",True,white)
text_1 = font.render("1",True,white)
text_2 = font.render("2",True,white)
text_3 = font.render("3",True,white)
text_4 = font.render("4",True,white)
text_5 = font.render("5",True,white)



def print_building():
	screen.fill(black)
	pygame.draw.line(screen, white, [640, SIZE], [0, SIZE], 3)
	pygame.draw.line(screen, white, [640, 2*SIZE], [0, 2*SIZE], 3)
	pygame.draw.line(screen, white, [640, 3*SIZE], [0, 3*SIZE], 3)
	pygame.draw.line(screen, white, [640, 4*SIZE], [0, 4*SIZE], 3)
	pygame.draw.line(screen, white, [640, 5*SIZE], [0, 5*SIZE], 3)
	pygame.draw.line(screen, white, [640, 6*SIZE], [0, 6*SIZE], 3)
	screen.blit(text_B1,(500, 6*SIZE-30))
	screen.blit(text_1,(500, 5*SIZE-30))
	screen.blit(text_2,(500, 4*SIZE-30))
	screen.blit(text_3,(500, 3*SIZE-30))
	screen.blit(text_4,(500, 2*SIZE-30))
	screen.blit(text_5,(500, SIZE-30))	

#clock = pygame.time.Clock()
pos_x = 200
pos_y = 400
print_building()
pygame.draw.rect(screen, red, [pos_x, pos_y, 25, SIZE], 5)
pygame.display.update()
while True:
	y=(input("B1, 1, 2, 3, 4, 5 중 택 1: "))
	if y == 'B1':
		y=500
	else:
		y=int(y)
		y+=1
		y=600-y*SIZE	
	print_building()
	pygame.display.update()
	if y == pos_y:
		print_building()
		pygame.draw.rect(screen, red, [pos_x, pos_y, 25, SIZE], 5)
		pygame.display.update()
	else:
		while y != pos_y:
			#clock.tick(10)
			if y <= pos_y:
				pos_y -= 4
			elif y >= pos_y:
				pos_y += 4
			print_building()
			pygame.draw.rect(screen, red, [pos_x, pos_y, 25, SIZE], 5)
			pygame.display.update()
			time.sleep(0.1)