import pygame
import sys
import random

def draw_floor():

	screen.blit(floor_surface, (floor_x_pos, 450))
	screen.blit(floor_surface, (floor_x_pos + 288, 450))


def create_pipe():

	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop =  (350, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom =  (350, random_pipe_pos - 150))
	return bottom_pipe, top_pipe


def move_pipes(pipes):

	for pipe in pipes:
		pipe.centerx -= 2.5

	return pipes


def draw_pipes(pipes):

	for pipe in pipes:

		if pipe.bottom >= 512:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)


def check_collision(pipes):

	for pipe in pipes:

		if bird_rect.colliderect(pipe):
			death_sound.play()
			return False

	if bird_rect.top <= -50 or bird_rect.bottom >= 450:
		death_sound.play()
		return False

	return True


def rotate_bird(bird):

	new_bird = pygame.transform.rotozoom(bird, -(bird_movement * 3), 1)
	return new_bird


def bird_animation():

	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))

	return new_bird, new_bird_rect


def score_display():

	score_surface = score_font.render(str(score), True, (255, 255, 255))
	score_rect = score_surface.get_rect(center = (144, 50))
	screen.blit(score_surface, score_rect)


def end_display():

	score_surface = score_font.render("SCORE : " + str(score), True, (255, 255, 255))
	score_rect = score_surface.get_rect(center = (144, 50))
	screen.blit(score_surface, score_rect)

	game_over_surface = pygame.image.load('sprites/message.png').convert_alpha()
	game_over_rect = game_over_surface.get_rect(center = (144, 256))
	screen.blit(game_over_surface, game_over_rect)

	text_surface = text_font.render("GAME OVER!", True, (255, 255, 255))
	text_rect = text_surface.get_rect(center = (144, 90))
	screen.blit(text_surface, text_rect)

	text_surface = text_font.render("PRESS SPACE TO PLAY AGAIN", True, (255, 255, 255))
	text_rect = text_surface.get_rect(center = (144, 420))
	screen.blit(text_surface, text_rect)


def first_display():

	first_game_surface = pygame.image.load('sprites/message.png').convert_alpha()
	first_game_rect = first_game_surface.get_rect(center = (144, 256))
	screen.blit(first_game_surface, first_game_rect)

	text_surface = text_font.render("PRESS SPACE TO PLAY!!!", True, (255, 255, 255))
	text_rect = text_surface.get_rect(center = (144, 420))
	screen.blit(text_surface, text_rect)


pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()

flap_sound = pygame.mixer.Sound('audio/wing.ogg')
death_sound =pygame.mixer.Sound('audio/hit.ogg')
score_sound = pygame.mixer.Sound('audio/point.ogg')

score_font = pygame.font.SysFont('comicsans', 40)
text_font = pygame.font.SysFont('comicsans', 27)

game_active = False
first_game = True

gravity = 0.125
up_speed = 4.5
bird_movement = 0

score = 0
high_score = 0

bg_surface = pygame.image.load('sprites/background-day.png').convert()
#bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('sprites/base.png').convert()
floor_x_pos = 0

bird_downflap = pygame.image.load('sprites/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('sprites/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('sprites/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50, 256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

'''bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert_alpha()
bird_rect = bird_surface.get_rect(center = (50, 256))'''

pipe_surface = pygame.image.load('sprites/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 225, 250, 275, 300, 325, 350, 375, 400]
current_pipe = 1
pipe_index_flag = False

while True:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_SPACE and game_active == True:
				bird_movement = 0
				bird_movement -= up_speed
				flap_sound.play()

			if event.key == pygame.K_SPACE and game_active == False:
				pipe_list.clear()
				current_pipe = 1
				score = 0
				pipe_index_flag = False
				bird_rect.center = (50, 256)
				bird_movement = 0
				game_active = True
				first_game = False

		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())
			pipe_index_flag = True

		if event.type == BIRDFLAP:

			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird_surface, bird_rect = bird_animation()
			

	screen.blit(bg_surface, (0, 0))

	if game_active:

		# Bird
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird, bird_rect)

		game_active = check_collision(pipe_list)

		# Pipes
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)

		if pipe_index_flag:
			if pipe_list[current_pipe].centerx + 40 <= bird_rect.centerx :
				score += 1
				score_sound.play()
				current_pipe += 2
				pipe_index_flag = False

		score_display()

	else:
		if first_game:
			first_display()
		else:
			end_display()

	# Floor
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -288:
		floor_x_pos = 0

	pygame.display.update()
	clock.tick(120)