import pygame
import random as rnd
from math import sqrt


x, y = 480, 480
low_x, low_y = -90, -150
high_x, high_y = 310, 100
scale_x, scale_y = 250, 250
distance = 100
step = 10
fps = 30

pygame.init()
screen = pygame.display
screen.set_mode((x, y))
clock = pygame.time.Clock()
screen.set_caption('Knights')
surf = screen.set_mode((x, y))


class Object(pygame.sprite.Sprite):
	def __init__(self, x = 480, y = 480):
		super().__init__()
		self.image = pygame.Surface((x, y))
		self.image.fill((100, 100, 100))
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.move_ip(*self.velocity)


class Wallpaper(pygame.sprite.Sprite):
	def __init__(self, file_name):
		self.rect = [0, 0]
		self.image = pygame.image.load('res/'+file_name)
		self.image = pygame.transform.scale(self.image, (x, y))


class Player(pygame.sprite.Sprite):
	def __init__(self, directory='', id=0):
		super().__init__()

		self.id = id
		self.picture = {}
		self.picture['idle'] = []
		self.picture['attack'] = []
		self.picture['walk'] = []

		for i in range(1, 5):
			self.picture['idle'].append(pygame.image.load('{}/idle{}.png'.format(directory, i)))
		for i in range(1, 5):
			self.picture['attack'].append(pygame.image.load('{}/attack{}.png'.format(directory, i)))
		for i in range(1, 5):
			self.picture['walk'].append(pygame.image.load('{}/walk{}.png'.format(directory, i)))

		self.cast = 0
		self.state = 'idle'
		self.side = False
		self.rect = [0, 0]
	
	def set(self, x, y):
		self.rect = [x, y]

	def move_x(self, step):
		self.rect[0] += step
		if step < 0: self.side = True
		elif step > 0: self.side = False
	
	def move_y(self, step):
		self.rect[1] += step
	
	def action(self, state):
		self.cast = 0
		self.state = state

	def update(self):
		self.cast = (self.cast + 1) % 16
		self.image = self.picture[self.state][self.cast // 4]
		self.image = pygame.transform.scale(self.image, (scale_x, scale_y))
		self.image = pygame.transform.flip(self.image, self.side, False)

		if self.rect[0] > high_x:
			self.set(high_x, self.rect[1])
		elif self.rect[0] < low_x:
			self.set(low_x, self.rect[1])
		if self.rect[1] > high_y:
			self.set(self.rect[0], high_y)
		elif self.rect[1] < low_y:
			self.set(self.rect[0], low_y)
	
	def is_hit(self, player):
		if sqrt((self.rect[0] - player.rect[0]) ** 2  + (self.rect[1] - player.rect[1]) ** 2) < distance:
			return True
		else: 
			return False

	def control(self, keys, obj):
		if keys[0] == True:
			if self.state != 'attack':
				self.action('attack')

			if self.cast // 4 == 2 and (self.side == (self.rect[0] >= obj.rect[0])) and self.is_hit(obj):
				obj.set(rnd.randint(low_x, high_x), rnd.randint(low_y, high_y))

		elif True in [keys[1], keys[2], keys[3], keys[4]]:
			if self.state != 'walk':
				self.action('walk')

			if keys[1] == True:
				self.move_x(-step)
			if keys[2] == True:
				self.move_x(step)
			if keys[3] == True:
				self.move_y(-step)
			if keys[4] == True:
				self.move_y(step)
		elif self.state != 'idle':
			self.action('idle')


wallpaper = Wallpaper('wallpaper.jpg')
pl1 = Player('player1', 1)
pl2 = Player('player2', 2)

while 1:
	clock.tick(fps)
	screen.update()
	screen.set_mode((y, x))

	# code itself
	pl1.update()
	pl2.update()
	# /

	surf.blit(wallpaper.image, wallpaper.rect)
	if pl1.rect[1] < pl2.rect[1]:
		surf.blit(pl1.image, pl1.rect)
		surf.blit(pl2.image, pl2.rect)
	else:
		surf.blit(pl2.image, pl2.rect)
		surf.blit(pl1.image, pl1.rect)

	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			pygame.quit()
	
	# controllers
	keys = pygame.key.get_pressed()
	keys_ = [
		keys[pygame.K_f], 
		keys[pygame.K_a], 
		keys[pygame.K_d], 
		keys[pygame.K_w], 
		keys[pygame.K_s]
	]
	pl1.control(keys_, pl2)

	keys_ = [
		keys[pygame.K_h], 
		keys[pygame.K_j], 
		keys[pygame.K_l], 
		keys[pygame.K_i], 
		keys[pygame.K_k]
	]
	pl2.control(keys_, pl1)

