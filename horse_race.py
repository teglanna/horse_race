import turtle
import random
import time


def getHorseImages(num_horses):
	images = []

	for i in range(0, num_horses):
		images = images + ['horse_' + str(i+1) + '_image.gif']

	return images

def getBannerImages(num_horses):
	all_images = []

	#get "They're off" banner image
	images = ['theyre_off_banner.gif']
	all_images.append(images)

	#get early lead banner images
	images = []
	for i in range(0, num_horses):
		images = images + ['lead_at_start_' + str(i+1) + '.gif']
	all_images.append(images)	

	#get mid-way lead banner images
	images = []
	for i in range(0, num_horses):
		images = images + ['looking_good_' + str(i+1) + '.gif']
	all_images.append(images)	

	#get "We Have a Winner" banner image
	images = ['winner_banner.gif']
	all_images.append(images)

	return all_images

def registerHorseImages(images):
	for i in range(0, len(images)):
		turtle.register_shape(images[i])

def registerBannerImages(images):
	for i in range(0, len(images)):
		for j in range(0, len(images[i])):
			turtle.register_shape(images[i][j])	

def newHorse(image_file):
	horse = turtle.Turtle()
	horse.hideturtle()
	horse.shape(image_file)

	return horse

def generateHorses(images, num_horses):
	horses = []
	for i in range(0, num_horses):
		horse = newHorse(images[i])
		horses.append(horse)

	return horses
	
def placeHorses(horses, loc, separation):
	for i in range(0, len(horses)):
		horses[i].hideturtle()
		horses[i].penup()
		horses[i].setposition(loc[0], loc[1] + i * separation)
		horses[i].setheading(180)
		horses[i].showturtle()
		horses[i].pendown()

def findLeadHorse(horses):
	lead_horse = 0
	for i in range(1, len(horses)):
		if horses[i].position()[0] < horses[lead_horse].position()[0]:
			lead_horse = i

	return lead_horse
	

def displayBanner(banner, position):
	the_turtle = turtle.getturtle()
	the_turtle.hideturtle()
	the_turtle.penup()
	the_turtle.setposition(position[0], position[1])	
	the_turtle.showturtle()		
	the_turtle.shape(banner)
	the_turtle.stamp()
	#hide default turtle and keep from drawing


def startHorses(horses, banners, finish_line, forward_incr):
	#init
	have_winner = False
	early_leading_horse_displayed = False
	midrace_leading_horse_displayed = False

	#display "They're off" banner image
	displayBanner(banner_images[0][0], (0, -300))

	i = 0
	while not have_winner:
		horse = horses[i]
		horse.forward(random.randint(1,3) * forward_incr)

		#display mid-race lead banner
		lead_horse = findLeadHorse(horses) # x should be less, because it decreases to the left
		if horses[lead_horse].position()[0] < -125 and not midrace_leading_horse_displayed:

			displayBanner(banners[2][lead_horse], (0, -300))
			early_leading_horse_displayed = True

		#display early lead banner
		elif horses[lead_horse].position()[0] < 125 and not early_leading_horse_displayed:
			displayBanner(banners[1][lead_horse], (0, -300))
			early_leading_horse_displayed = True	


		#check for horse over finish line
		if horse.position()[0] < finish_line:
			have_winner = True
		else:
			i = (i+1) % len(horses) #keep going round and round, from horse_1 to horse_10
	return i
	

def displayWinner(winning_horse, winner_banner):
	#display "We have a Winner" banner
	displayBanner(winner_banner, (0, -300))

	#blink winning horse
	show = False
	blink_counter = 5
	while blink_counter != 0:
		if show:
			winning_horse.showturtle()
			show = False
			blink_counter = blink_counter - 1
		else:
			winning_horse.hideturtle()
			show = True

		time.sleep(.4)


# ---- main	
#init number of horses
num_horses = 10

#set window size
turtle.setup(750, 750)

#get turtle window
window = turtle.Screen()
window.title('Horse Race')

#init screen layout parameters
start_loc = (240, -220)
track_separation = 60
finish_line = -240
forward_incr = 6

#register images
horse_images = getHorseImages(num_horses)
banner_images = getBannerImages(num_horses)
registerHorseImages(horse_images)
registerBannerImages(banner_images)

#generate and init horses
horses = generateHorses(horse_images, num_horses)

# place horses at starting line
placeHorses(horses, start_loc, track_separation)

#start horses
winner = startHorses(horses, banner_images, finish_line, forward_incr)

#light up for winning horse
displayWinner(horses[winner], banner_images[3][0])

#terminate program when close window
turtle.exitonclick()				
