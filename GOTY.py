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

class Game():

	Loops = [
		{'control_type': 'beginner'},
		{'control_type': 'advanced'},
		{'control_type': 'advanced', 'move_screen': True}
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

		try:
			self.web_browser = webbrowser.get('chromium-browser')
		except:
			try: self.web_browser = webbrowser.get()
			except: print("Could not get web browser")

		self.popup()

		self.move_screen = False

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

		self.level = 1
		self.loop_number = 0
		self.loop(self.loop_number)

		self.level_maker.render_level(self.level)

		while True: 
			self.update()

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.display.quit()
				pygame.quit()
				sys.exit()

		self.screen.fill(self.background_color)
		self.all_sprites.update()
		self.all_sprites.draw(self.screen)

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
		print(self.loop_number, loopNumber)
		if loopNumber is not None: 
			self.loop_number = loopNumber
		elif loopNumber is None: 
			self.loop_number += 1
		
		self.level = 1
		print(self.loop_number)
		loop_info = Game.Loops[min(self.loop_number, len(Game.Loops)-1 )]
		print(loop_info)
		
		self.player.control_type = loop_info['control_type']

		if loop_info.get('move_screen'):
			self.move_screen = loop_info['move_screen']

	def popup(self):  
		self.web_browser.open("http://foxnews.com", new=1, autoraise=False)
		os.system("wmctrl -a " + self.window_name)

	def move_display(self, move_direction):
		os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' %tuple(move_direction)
		pygame.display.set_mode(self.screen_size[0])

game = Game()
