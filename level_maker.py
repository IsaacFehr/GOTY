import pygame
import re
from levels import Levels

Borders = [
	{'type': 'rect', 'position': (0,-1), 'size': ("100%", 1), 'fills': None},
	{'type': 'rect', 'position': ("100%+1",0), 'size': (1, "100%"), 'fills': None},
	{'type': 'rect', 'position': (0,"100%+1"), 'size': ("100%", 1), 'fills': None, 'kill': True},
	{'type': 'rect', 'position': (-1,0), 'size': (1, "100%"), 'fills': None},
]

class LevelMaker(pygame.sprite.Group):

	COLORKEY = pygame.Color('aliceblue')
	TEXT_Y = 100

	def __init__(self, game):
		super().__init__()
		self.colorkey = LevelMaker.COLORKEY
		self.game = game

		self.text_y = LevelMaker.TEXT_Y
		self.font = pygame.font.Font(None, 100)
		self.level_number_text = pygame.sprite.Sprite(self.game.all_sprites)

	def render_level(self, level_number):
		self.clear_level()
		level = Levels[level_number]

		self.update_text("LEVEL " + str(level_number))

		level_sprites = level['sprites']
		level_sprites.extend(Borders)
		
		for sprite_info in level['sprites']:
			sprite = pygame.sprite.Sprite(self)
			position, size = self.calculate_rect(sprite_info)
			sprite.image = pygame.Surface(size)
			sprite.rect = sprite.image.get_rect()
			sprite.rect.topleft = position
			self.draw_shape(sprite, sprite_info)
			self.game.all_sprites.add(sprite)

	def update_text(self, text):
		self.level_number_text.image = self.font.render(text, True, pygame.color.Color('white'))
		self.level_number_text.rect = self.level_number_text.image.get_rect()
		self.level_number_text.rect.center = (self.game.screen_size[0]/2, self.text_y)

	def clear_level(self):
		for sprite in iter(self):
			sprite.kill()
		self.empty()

	def calculate_rect(self, sprite_info ):
		position = []
		size = []
		rect_info = (position, size)

		info = (sprite_info['position'], sprite_info['size'])
		for attribute, attr_info in enumerate(info):
			for index, value in enumerate(attr_info):
				if type(value) == str:
					value = self.parse_value(value, index)
				rect_info[attribute].append(value)

		return rect_info

	def parse_value(self, valString, direction):
		operator = re.search(r'[\+\-]', valString)
		if operator: operator = operator.group()

		if operator: values = valString.split(operator)
		else: values = [valString]
		for index, value in enumerate(values):
			value = value.strip()
			if value.find('%') is not -1: values[index] = self.calculate_percentage(value, direction)
			else: values[index] = float(value)
		if operator == '+':
			return values[0] + values[1]
		elif operator == '-':
			return values[0] - values[1]
		else:
			return values[0]

	def calculate_percentage(self, percentage, direction ):
		percentage = float(percentage.rstrip('%'))
		return ( self.game.screen_size[direction] * (percentage / 100.0) )

	def draw_shape(self, sprite, sprite_info):
		fills = []
		if sprite_info.get('fills'):
			for color in sprite_info['fills']:
				fills.append( pygame.Color(color) )
		else: fills.append( pygame.Color(0,0,0,255) )

		surface = sprite.image
		size = sprite.rect.size

		if sprite_info.get('kill'):
			self.game.killers.add(sprite)

		surface.set_colorkey(self.colorkey)
		surface.fill(self.colorkey)

		sprite_type = sprite_info['type']
		if sprite_type == 'rect':
			surface.fill(fills[0])
		elif sprite_type == 'goal':
			pygame.draw.rect(surface, fills[0], (0, 0, 10, size[1]))
			pygame.draw.polygon(surface, fills[1], ((10,0),(size[0], 20),(10,40)) )
			self.game.goals.add(sprite)
		elif sprite_type == 'spike':
			pygame.draw.polygon(surface, fills[0], ((0,size[1]),(size[0]/2,0),(size[0],size[1])) )
			self.game.killers.add(sprite)





