import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy as np

pygame.init()
DISPLAY_WIDTH=800
DISPLAY_HEIGHT=600
dis=pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('Pandemic Simulator')

## Defining necessary variables
## ----------------------------

## Defining Colors
BLUE1=(230,230,250) #background color1
BLUE2=(173,216,230) #background color2
RED=(255,0,0) #known infected
Black=(0,0,0) #known dead
GREEN=(0,255,0) #known healed
WHITE=(255,255,255) #Never sick
ORANGE=(255,165,0) #unknown infected
DARKGREEN=(0,100,0) #unkown healed
BLUE=(0,0,255) #unknown dead
COLOR_INACTIVE = pygame.Color('lightskyBLUE3') #Color for inputboxes
COLOR_ACTIVE = pygame.Color('dodgerBLUE2') #Color for inputboxes


## Defining the necessary functions for the Display of the Simulation
## ------------------------------------------------------------------


## Text Objects

SMALLFONT = pygame.font.SysFont("comicsansms", 15)
MEDFONT = pygame.font.SysFont("comicsansms", 20)
LARGEFONT = pygame.font.SysFont("comicsansms", 25)
VERYSMALLFONT = pygame.font.SysFont("comicsansms", 12)

def text_objects(text,color,size):
    if size == "small":
        textSurface = SMALLFONT.render(text, True, color)
    elif size == "medium":
        textSurface = MEDFONT.render(text, True, color)
    elif size == "large":
        textSurface = LARGEFONT.render(text, True, color)
    elif size == 'very small':
	    textSurface = VERYSMALLFONT.render(text, True, color)

    return textSurface, textSurface.get_rect()
    
   
def message_to_screen(msg,color=Black, x=0, y=0, size = "medium"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = x, y
    dis.blit(textSurf, textRect)
	
## Drawing all People on Board
def draw_infected(color):
	global dis
	xvalue=1
	i=0
	while xvalue<782:
		yvalue=101
		while yvalue<582:
			pygame.draw.rect(dis,color[i],[xvalue,yvalue,18,18])
			pygame.draw.rect(dis,Black,[xvalue,yvalue,18,18], 1)
			yvalue=yvalue+20
			i=i+1
		xvalue=xvalue+20
		

## Defining some functions for simulation
## -----------------------------------------
##
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

## Running the Simulation
## ----------------------
def simulation_loop():
	global dis
	settings=True
	simulation=False
	simulation_exit=False
	final_screen=False
	
	while not simulation_exit:

		#Definition Input boxes for Settings Screen
		active1 = False
		active2 = False
		active3 = False
		active4 = False
		active5 = False
		people = "5"
		death_rate_percent = "20"
		infectiousness = "2"
		recovery_rate ="14"
		contacts = '70'
		
		while settings:
		
			#Drawing the Settings Screen
			
			input_box1 = pygame.Rect((DISPLAY_WIDTH//2+30), 190, 200, 32)
			input_box2 = pygame.Rect((DISPLAY_WIDTH//2+30), 240, 200, 32)
			input_box3 = pygame.Rect((DISPLAY_WIDTH//2+30), 290, 200, 32)
			input_box4 = pygame.Rect((DISPLAY_WIDTH//2+30), 340, 200, 32)
			input_box5 = pygame.Rect((DISPLAY_WIDTH//2+30), 390, 200, 32)
			start_box = pygame.Rect((DISPLAY_WIDTH//2)-217,475,430,50)

			
			#Click events in Settings Box
			for event in pygame.event.get():
				#Closing Game when X in upper right is pressed
				if event.type == pygame.QUIT:
					settings = False
					simulation_exit = True    
				if event.type == pygame.MOUSEBUTTONDOWN:
					#When Press start is pressed, go out of settings window
					if start_box.collidepoint(event.pos):
						settings = False
						simulation= True
					#Input boxes acknowledge they are being used
					elif input_box1.collidepoint(event.pos):
						active1 = not active1
						active2 = False
						active3 = False
						active4 = False
						active5 = False
					elif input_box2.collidepoint(event.pos):
						active1 = False
						active2 = not active2
						active3 = False
						active4 = False
						active5 = False
					elif input_box3.collidepoint(event.pos):
						active1 = False
						active2 = False
						active3 = not active3
						active4 = False
						active5 = False
					elif input_box4.collidepoint(event.pos):
						active1 = False
						active2 = False
						active3 = False
						active4 = not active4
						active5 = False
					elif input_box5.collidepoint(event.pos):
						active1 = False
						active2 = False
						active3 = False
						active4 = False
						active5 = not active5
					else:
						active1 = False
						active2 = False
						active3 = False
						active4 = False
						active5 = False
				#Inputting text to Input boxes
				if event.type == pygame.KEYDOWN:
					if active1:
						if event.key == pygame.K_RETURN:
							active1 = False
						elif event.key == pygame.K_BACKSPACE:
							people = people[:-1]
						else:
							people += event.unicode
					if active2:
						if event.key == pygame.K_RETURN:
							active2 = False
						elif event.key == pygame.K_BACKSPACE:
							contacts = contacts[:-1]
						else:
							contacts += event.unicode
					if active3:
						if event.key == pygame.K_RETURN:
							active3 = False
						elif event.key == pygame.K_BACKSPACE:
							death_rate_percent = death_rate_percent[:-1]
						else:
							death_rate_percent += event.unicode
					if active4:
						if event.key == pygame.K_RETURN:
							active4 = False
						elif event.key == pygame.K_BACKSPACE:
							infectiousness = infectiousness[:-1]
						else:
							infectiousness += event.unicode
					if active5:
						if event.key == pygame.K_RETURN:
							active5 = False
						elif event.key == pygame.K_BACKSPACE:
							recovery_rate = recovery_rate[:-1]
						else:
							recovery_rate += event.unicode
				
				input_color1 = COLOR_ACTIVE if active1 else COLOR_INACTIVE
				input_color2 = COLOR_ACTIVE if active2 else COLOR_INACTIVE
				input_color3 = COLOR_ACTIVE if active3 else COLOR_INACTIVE
				input_color4 = COLOR_ACTIVE if active4 else COLOR_INACTIVE
				input_color5 = COLOR_ACTIVE if active5 else COLOR_INACTIVE
			
			#Reset input if it isn't in allowed range or some input a random string that is not a number
			if not active1:
				if not isfloat(people):
					people='5'
				elif float(people)<0.1 or float(people)>10000:
					people = "5"
			if not active2:
				if not isfloat(contacts):
					contacts ='70'
				elif float(contacts) not in list(np.arange(1, 1001, 1)):
					contacts = '70'
			if not active3:
				if not isfloat(death_rate_percent):
					death_rate_percent = "20"
				elif float(death_rate_percent)<0 or float(death_rate_percent)>100:
					death_rate_percent = "20"
			if not active4:
				if not isfloat(infectiousness):
					infectiousness ="2"
				elif float(infectiousness)<0 or float(infectiousness)>100:
					infectiousness = "2"
			if not active5:
				if not isfloat(recovery_rate):
					recovery_rate ="14"
				elif float(recovery_rate) not in list(np.arange(1, 101, 1)):
					recovery_rate ="14"
			
			
			
			#Actually writing the text thats inside the input boxes+ the boxes itself
			dis.fill(WHITE)
			message_to_screen("Please enter the settings for your Pandemic Simulation", Black, DISPLAY_WIDTH//2, 100, 'large')
			message_to_screen("Population (Mio.)", Black, (DISPLAY_WIDTH//2)-200, 200)
			message_to_screen("(0.1-10000)", Black, (DISPLAY_WIDTH//2)+300, 200)
			message_to_screen("Amount of contagious contacts per week", Black, (DISPLAY_WIDTH//2)-200, 250)
			message_to_screen("(1-1000)", Black, (DISPLAY_WIDTH//2)+300, 250)
			message_to_screen("Healthcare level/Death rate (%)", Black, (DISPLAY_WIDTH//2)-200, 300)
			message_to_screen("(0-100)", Black, (DISPLAY_WIDTH//2)+300, 300)
			message_to_screen("For example: Germany 5%, USA 21%", Black, (DISPLAY_WIDTH//2)-200, 325, "small")
			message_to_screen("Chance of contracting Virus per contact (%)", Black, (DISPLAY_WIDTH//2)-200, 350)
			message_to_screen("Recommended Values (1-5)", Black, (DISPLAY_WIDTH//2)-200, 375, "small")
			message_to_screen("(0-100)", Black, (DISPLAY_WIDTH//2)+300, 350)
			message_to_screen("Recovery Rate (days)", Black, (DISPLAY_WIDTH//2)-200, 400)
			message_to_screen("(1-100)", Black, (DISPLAY_WIDTH//2)+300, 400)
			message_to_screen("For example: Corona = 14", Black, (DISPLAY_WIDTH//2)-200, 425, "small")
			message_to_screen("Press HERE to start the Simulation!", RED, (DISPLAY_WIDTH//2), 500, "large")
			message_to_screen(people, x=input_box1.x+100, y=input_box1.y+15)
			message_to_screen(contacts, x=input_box2.x+100, y=input_box2.y+15)
			message_to_screen(death_rate_percent, x=input_box3.x+100, y=input_box3.y+15)
			message_to_screen(infectiousness, x=input_box4.x+100, y=input_box4.y+15)
			message_to_screen(recovery_rate, x=input_box5.x+100, y=input_box5.y+15)
			pygame.draw.rect(dis, input_color1, input_box1, 2)
			pygame.draw.rect(dis, input_color2, input_box2, 2)
			pygame.draw.rect(dis, input_color3, input_box3, 2)
			pygame.draw.rect(dis, input_color4, input_box4, 2)
			pygame.draw.rect(dis, input_color5, input_box5, 2)
			pygame.draw.rect(dis,Black,start_box, 1)
			pygame.display.update()
			
			
		#Additional Seetings for Simulation:
		day =1
		lockdownday=1
		alldead = False
		lockdown = False
		day1confirmed = (float(people)*10)
		confirmedinfected =[int(day1confirmed)]
		new_infected = [int(day1confirmed)]
		confirmeddead=[0]
		confirmedrecoveRED = [0]
		total_cases = [int(day1confirmed)]
		dead_people = 0
		recoveRED_people = 0
		dis=pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
		while simulation:
			squarelist =[]
		
			## Interface
			#Drawing background and top
			dis.fill(BLUE1)
			pygame.draw.rect(dis,BLUE2,[0,0,800,100])
			pygame.draw.rect(dis,Black,[0,0,800,100], 1)
			message_to_screen("Showing 1% of the actual population | Day 1 = 1/100000 of population confirmed infected ", Black, (DISPLAY_WIDTH//2), 8, 'small')
			
			#legend
			pygame.draw.rect(dis,Black,[215,80,18,18])
			pygame.draw.rect(dis,Black,[215,80,18,18], 1)
			message_to_screen("Dead", x=255, y=89, size='small')
			pygame.draw.rect(dis,RED,[285,80,18,18])
			pygame.draw.rect(dis,Black,[285,80,18,18], 1)
			message_to_screen("Infected", x=340, y=89, size='small')
			pygame.draw.rect(dis,WHITE,[500,80,18,18])
			pygame.draw.rect(dis,Black,[500,80,18,18], 1)
			message_to_screen("Healthy", x=550, y=89, size='small')
			pygame.draw.rect(dis,GREEN,[390,80,18,18])
			pygame.draw.rect(dis,Black,[390,80,18,18], 1)
			message_to_screen("RecoveRED", x=450, y=89, size='small')
			
			#Buttons
			pygame.draw.rect(dis,WHITE,[10,59,100,20])
			finish_box = pygame.draw.rect(dis,Black,[10,59,100,20], 1)
			message_to_screen("Finish", x=60, y=69, size='small')
			pygame.draw.rect(dis,WHITE,[690,59,100,20])
			Nextday_box = pygame.draw.rect(dis,Black,[690, 59, 100, 20], 1)
			message_to_screen("NEXT DAY", x=740, y=69, size='small')
			if not lockdown:
				pygame.draw.rect(dis,WHITE,[420,59,260,20])
				germanlock_box = pygame.draw.rect(dis,Black,[420, 59, 260, 20], 1)
				message_to_screen("German Lockdown: Contacts -> 5", x=550, y=69, size='small')
				pygame.draw.rect(dis,WHITE,[130,59,260,20])
				americanlock_box = pygame.draw.rect(dis,Black,[130, 59, 260, 20], 1)
				message_to_screen("American Lockdown: Contacts -> 10", x=260, y=69, size='small')
			elif lockdown:
				message_to_screen(f"You initiated lockdown on day {lockdownday}", x=400, y=69, size='small', color=RED)
				
			#Settings
			message_to_screen(f"| Population (Mio.): {people} | Death rate: {death_rate_percent}% | Contagiousness: {infectiousness}% | Contacts per week: {contacts} | Days till Recovery: {recovery_rate} |", x=400, y=49, size='very small')
			
			#Stats
			message_to_screen(f"| Cases: {total_cases[day-1]} | Currently Infected: {confirmedinfected[day-1]} | Deaths: {confirmeddead[day-1]} | Day {day} |", color=RED, x=400, y=29, size='small')
			
				
			for event in pygame.event.get():
				#Closing Game when X in upper right is pressed
				if event.type==pygame.QUIT:
					simulation_exit=True
					simulation = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					#When Reset is pressed go to Settings Window
					if finish_box.collidepoint(event.pos):
						final_screen = True
						simulation= False
					#When lockdowns are pressed change Infectiousness	
					if germanlock_box.collidepoint(event.pos) and not lockdown:
						contacts = "7"
						lockdown = True
						lockdownday = day
					if americanlock_box.collidepoint(event.pos) and not lockdown:
						contacts = "21"
						lockdown = True
						lockdownday = day
						
					#This is where the program basically starts
					if Nextday_box.collidepoint(event.pos):
						new_cases = confirmedinfected[day-1]*(((1+(float(infectiousness)/100))**(float(contacts)/7))-1)
						infected_people = confirmedinfected[day-1] +new_cases
						
						#recoverd people are no longer infected after recovery time
						if day >= int(recovery_rate):
							infected_people = infected_people - new_infected[day-int(recovery_rate)]
							dead_people = dead_people + new_infected[day-int(recovery_rate)] *(int(death_rate_percent)/100)
							recoveRED_people = recoveRED_people + new_infected[day-int(recovery_rate)] *(1-(int(death_rate_percent)/100))
							
						confirmeddead.append(int(dead_people))
						confirmedrecoveRED.append(int(recoveRED_people))
						confirmedinfected.append(int(infected_people))
						total_cases.append(int(total_cases[day-1]+new_cases))
						new_infected.append(int(new_cases))
						
						#When total_cases become more than the population:
						if total_cases[day] > int(people)*1000000:
							alldead = True
							final_screen = True
							simulation= False
							total_cases[day]=int(people)*1000000
							confirmedinfected[day] = total_cases[day] - confirmeddead[day] - confirmedrecoveRED[day]
						
							
						day = day +1
				
			## Draw the squares onto simulation
			#Define the amount of squares for dead + recoveRED + infected
			deadnr = int(confirmeddead[day-1]/(float(people)*10))
			if (confirmeddead[day-1]/(float(people)*10)) % 1 >=0.5:
				deadnr = deadnr+1
			infectednr = int(confirmedinfected[day-1]/(float(people)*10))
			if (confirmedinfected[day-1]/(float(people)*10)) %1 >=0.5:
				infectednr = infectednr+1
			recoveREDnr = int(confirmedrecoveRED[day-1]/(float(people)*10))
			if (confirmedrecoveRED[day-1]/(float(people)*10)) % 1 >=0.5:
				recoveREDnr = recoveREDnr+1
			#Attach amount of squares to list that have to be coloRED
			for i in range(0, infectednr):
				squarelist.append(RED)
			for i in range(0, deadnr):
				squarelist.append(Black)
			for i in range(0, recoveREDnr):
				squarelist.append(GREEN)
			# If list is to long, truncate
			if len(squarelist)>1000:
				for i in range(0, len(squarelist) - 1000 ): 
					squarelist.pop()
			#	If to few people infected, fill list with uninfected (WHITE)
			elif len(squarelist)<1000:
				while len(squarelist)<1000:
					squarelist.append(WHITE)
			draw_infected(squarelist)					
			pygame.display.update()
			
		while final_screen:
		
			# Drawing the Final Screen
			dis.fill(BLUE1)
			message_to_screen("Thanks for using my Pandemic Simulator", Black, (DISPLAY_WIDTH//2), 50, 'large')
			message_to_screen("by Tobias Beeth", Black, (DISPLAY_WIDTH//2), 100, 'medium')
			pygame.draw.rect(dis,WHITE,[200,250,150,40])
			quit_box = pygame.draw.rect(dis,Black,[200,250,150,40], 1)
			message_to_screen("Quit", x=275, y=270, size='large')
			pygame.draw.rect(dis,WHITE,[450,250,150,40])
			Reset_box = pygame.draw.rect(dis,Black,[450, 250, 150, 40], 1)
			message_to_screen("Reset", x=525, y=270, size='large')
			#pygame.draw.rect(dis,WHITE,[275,350,250,40])
			#stats_box = pygame.draw.rect(dis,Black,[275, 350, 250, 40], 1)
			#message_to_screen("View Stats", x=400, y=370, size='large')
			message_to_screen(f"| Cases: {total_cases[day-1]} | Currently Infected: {confirmedinfected[day-1]} | Deaths: {confirmeddead[day-1]} | Day {day} |", color=RED, x=400, y=200, size='medium')
			message_to_screen(f"| Population (Mio.): {people}  Death rate: {death_rate_percent}% | Contagiousness: {infectiousness}% | Contacts per week: {contacts} | Days till Recovery: {recovery_rate} |", x=400, y=160, size='very small')
			if alldead:
				message_to_screen("Everyone has been infected", RED, (DISPLAY_WIDTH//2), 450, 'large')
			
			for event in pygame.event.get():
				#Closing Game when X in upper right is pressed
				if event.type==pygame.QUIT:
					simulation_exit=True
					final_screen = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					# When reset box is pressed go to settings screen
					if Reset_box.collidepoint(event.pos):
						final_screen = False
						settings= True
					#when quit box is pressed quit
					if quit_box.collidepoint(event.pos):
						final_screen = False
						simulation_exit= True
					#when stats box is pressed, quit and show sztats
					#if stats_box.collidepoint(event.pos):
					#	final_screen = False
					#	simulation_exit= True
						
			pygame.display.update()
	pygame.quit()
	quit()
 
simulation_loop()
