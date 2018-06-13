import os, sys
import math
import random
import pygame
import pygame.freetype
from pygame.locals import *
import webbrowser
import time

from level_maker import LevelMaker
from levels import Levels
from player import Player

INITIAL_SCREEN_DIMENSIONS = (800, 500)
FPS = 30
BACKGROUND_COLOR = pygame.Color('blue')
WINDOW_NAME = "G.O.T.Y."
MESSAGE_Y = 200
DISPLAY_TOPLEFT = (100,100)

class Game():

	Loops = [
		{'control_type': 'beginner', 'message': "arrow keys and spacebar will get you where you need to go"},
		{'control_type': 'advanced', 'message': "LOOP 1: switching to pro controls; input with key presses: siniSTER, DEXter, and HOP"},
	]

	def __init__(self):
		self.fps = FPS
		self.screen_size = INITIAL_SCREEN_DIMENSIONS

		#Initialize PyGame
		self.clock = pygame.time.Clock()
		pygame.init()
		frame_delay = int(1000 / self.fps)
		#pygame.key.set_repeat( frame_delay, frame_delay) #Held keys will fire an event every frame
		self.screen = pygame.display.set_mode(self.screen_size)
		self.window_name = WINDOW_NAME
		pygame.display.set_caption(self.window_name)

		self.move_screen = False
		self.display_topleft = DISPLAY_TOPLEFT
		self.display_move_delta = [0,0]
		self.keys_down = None

		pygame.font.init()
		self.message_font = pygame.font.Font(None, 24)
		self.message_y = MESSAGE_Y

		try:
			self.web_browser = webbrowser.get('chromium-browser')
		except:
			try: self.web_browser = webbrowser.get()
			except: print("Could not get web browser")

		self.popup()

		self.background_color = BACKGROUND_COLOR

		#Initialize sprite groups
		self.all_sprites = pygame.sprite.Group()
		self.goals = pygame.sprite.Group()
		self.killers = pygame.sprite.Group()

		self.level_maker = LevelMaker(self)

		self.player = Player(self)

		self.players = pygame.sprite.Group()
		self.players.add(self.player)
		self.all_sprites.add(self.player)

		self.message = pygame.sprite.Sprite(self.all_sprites)

		self.level = 1
		self.loop_number = 0
		self.loop(self.loop_number)

		self.level_maker.render_level(self.level)

		self.move_display((0,0))

		while True: 
			self.update()

	def update(self):
		for event in pygame.event.get():
			#print(event)
			if event.type == QUIT:
				pygame.display.quit()
				pygame.quit()
				sys.exit()
			elif event.type == ACTIVEEVENT:
				if self.keys_down:
					for key in self.keys_down:
						keyUpEvent = pygame.event.Event(KEYUP, {'unicode': key, 'key': self.player.key_dict[key], 'mod':0})
						keyDownEvent = pygame.event.Event(KEYDOWN, {'unicode': key, 'key': self.player.key_dict[key], 'mod':0, 'scancode': 0})
						#pygame.event.post(keyUpEvent)
						pygame.event.post(keyDownEvent)
					self.key_down = None


		self.screen.fill(self.background_color)
		self.all_sprites.update()
		self.all_sprites.draw(self.screen)

		if self.display_move_delta != [0,0]:
			self.move_display(self.display_move_delta)
			self.display_move_delta = [0,0]

		pygame.display.update()
		self.clock.tick(self.fps)

	def levelup(self):
		if self.level < len(Levels.keys()):
			self.level += 1
		else:
			self.loop()
		self.level_maker.render_level(self.level)
		self.player.spawn()
		#self.popup()

	def loop(self, loopNumber = None):
		if loopNumber is not None: 
			self.loop_number = loopNumber
		elif loopNumber is None: 
			self.loop_number += 1
		
		self.level = 1
		loop_info = Game.Loops[min(self.loop_number, len(Game.Loops)-1 )]

		self.display_message(loop_info['message'])
		
		self.player.control_type = loop_info['control_type']

		if loop_info.get('move_screen'):
			self.move_screen = loop_info['move_screen']

	def display_message(self, text):
		self.message.image = self.message_font.render(text, True, pygame.color.Color('white'))
		self.message.rect = self.message.image.get_rect()
		self.message.rect.center = (self.screen_size[0]/2, self.message_y)

	def popup(self):  
		self.web_browser.open("http://foxnews.com", new=1, autoraise=False)
		os.system("wmctrl -a " + self.window_name)

	def move_display(self, move_direction):
		new_topleft = (self.display_topleft[0] + move_direction[0], self.display_topleft[1] + move_direction[1])
		os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' %new_topleft
		self.display_topleft = new_topleft
		
		if pygame.display.get_surface().get_rect().size == self.screen_size:
			pygame.display.set_mode( (self.screen_size[0]-1,self.screen_size[1]-1))
		else:
			pygame.display.set_mode(self.screen_size)

game = Game()
