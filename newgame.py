import pygame
import time
import random

pygame.init()

display_width=900
display_height=750

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
color_list=[black,red,blue,green]

car_width=65
car_height=140

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('CAR CRUNCH')
clock=pygame.time.Clock()

carImg=pygame.image.load("scarunit.jpg")


def things(thingx,thingy,thingw,thingh,color):
	pygame.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])


def car(x,y):
	gameDisplay.blit(carImg,(x,y))


def text_objects(text,font):
	textSurface=font.render(text,True,red)
	return textSurface, textSurface.get_rect()

def message_display(text):
	largeText=pygame.font.Font('freesansbold.ttf',50)
	TextSurf, TextRect=text_objects(text,largeText)
	TextRect.center=((display_width/2),(display_height/2))
	gameDisplay.blit(TextSurf,TextRect)

	pygame.display.update()


def crash():
	message_display("YOU CRASHED!")
	time.sleep(2)
	game_loop()


def things_dodged(count,color):
	font=pygame.font.SysFont(None,35)
	text=font.render("Dodged: "+str(count),True,color)
	gameDisplay.blit(text,(10,10))

def game_level(level,color):
	levelfont=pygame.font.SysFont(None,35)
	leveltext=levelfont.render("Level: "+str(level),True,color)
	level_width=leveltext.get_width()
	gameDisplay.blit(leveltext,(display_width-level_width-10,10))


def game_loop():

	y=display_height*0.75
	x=display_width*0.45

	dodged=0
	level=1

	gameExit=False

	x_change=0
	list=[] #using as a stack for car movement
	length=0 #length of list
	color=(0,0,0)
	

	#for obrstructive moving things
	thing_width=100
	thing_height=100
	thing_startx=random.randrange(0,display_width-thing_width)
	thing_starty=-600
	thing_speed=8
	thing_count=0


	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			#car movement code
			if event.type == pygame.KEYDOWN:
				if event.key==pygame.K_LEFT:
					if length==0 or list[length-1]!=-1: 
						list.append(-1)
						length+=1
					x_change=-5
					
				if event.key==pygame.K_RIGHT:
					if length==0 or list[length-1]!=1:
						list.append(1)
						length+=1
					x_change=5

			if event.type == pygame.KEYUP:
				if length==0:
						x_change=0
			
				elif length==1:
					if event.key==pygame.K_LEFT:
						if list[0]==1:
							x_change=5
						elif list[0]==-1:
							list.pop()
							length-=1
							x_change=0
					if event.key==pygame.K_RIGHT:
						if list[0]==-1:
							x_change=-5
						elif list[0]==1:
							list.pop()
							length-=1
							x_change=0

				elif length==2:
					if event.key==pygame.K_LEFT:
						list.remove(-1)
						length-=1
						x_change=5
					if event.key==pygame.K_RIGHT:
						list.remove(1)
						length-=1
						x_change=-5



		x+=x_change
		thing_starty+=thing_speed

		#things regernerate	
		if thing_starty>display_height:
			thing_starty=0-thing_height
			thing_startx=random.randrange(0,display_width-thing_width)
			#dodged score
			dodged+=1
			#level and color change
			if dodged%4==0:
				level+=1
				color=random.choice(color_list)
			#changing difficulty of level
			if level>=2:
				#thing_width+=(dodged*2)#difficulty by width increase
				if level>=3:
					thing_speed+=1#difficulty by speed increase


		#crashed by walls
		if x<0 or x+car_width>display_width:
			crash()

		#crashed by other cars
			# y coordinates crossover
		if y<=thing_starty+thing_height and y+car_height>=thing_starty: 
				# x coordinates crossover
			if x>=thing_startx and x<=thing_startx+thing_width or x+car_width>=thing_startx and x+car_width<=thing_startx+thing_width or thing_startx>=x and thing_startx+thing_width<=x+car_width:
				pass#crash()
				

		#new frame starts here
		gameDisplay.fill(white)

		car(x,y)
		things_dodged(dodged,color)
		game_level(level,color)
		things(thing_startx,thing_starty,thing_width,thing_height,color)
		


		pygame.display.update() #applies all the updates made to the frame by updating full frame display
		clock.tick(60)

game_loop()