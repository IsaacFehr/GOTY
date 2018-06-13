import pygame
import pygame
from pygame.locals import *
import numpy

class Player(pygame.sprite.Sprite):

	CHARACTER_SIZE = (50, 50)
	CHARACTER_COLOR = pygame.Color("red")
	MAX_VELOCITY = (10, 20)
	JUMP_VELOCITY = (0, -13)
	RUN_ACCELERATION = (1, 0)
	FRICTION = 0.5
	GRAVITY = (0, 1)
	SPAWN_POSITION = (50,50)

	def __init__(self, game):
		super().__init__()
		self.game = game

		self.control_type = 'beginner'

		self.spawn_position = Player.SPAWN_POSITION
		self.size = Player.CHARACTER_SIZE
		self.color = Player.CHARACTER_COLOR
		self.jump_velocity = Player.JUMP_VELOCITY

		self.image = pygame.Surface( self.size )
		self.rect = self.image.get_rect()
		self.draw_self()

		self.key_dict = self.init_key_dict()

		self.velocity = [0, 0]
		self.max_velocity = Player.MAX_VELOCITY

		self.run_acceleration = Player.RUN_ACCELERATION
		self.friction = Player.FRICTION

		self.gravity = Player.GRAVITY
		self.is_grounded = False

		self.spawn()

	def update(self):
		self.handle_input()
		self.apply_gravity()
		self.apply_friction()
		self.update_position()
		self.check_collision()
		self.draw_self()

	def spawn(self):
		self.rect.topleft = self.spawn_position
		self.velocity = [0,0]
		self.is_grounded = False

	def kill(self):
		self.spawn()

	def draw_self(self):
		self.image.fill( self.color )

	def handle_input(self):
		if pygame.key.get_focused():
			move_direction = [0, 0]
			pressed_keys = pygame.key.get_pressed()
			if self.control_type == 'beginner':
				move_direction[0] = pressed_keys[K_RIGHT] - pressed_keys[K_LEFT]
				self.run(move_direction)
				if pressed_keys[K_SPACE]: self.jump()
			elif self.control_type == 'advanced':
				move_direction[0] = self.check_held_keys("dex", pressed_keys) - self.check_held_keys("ster", pressed_keys)
				if move_direction != [0,0]:
					self.run(move_direction)
				if self.check_held_keys("hop", pressed_keys): self.jump()

	def check_held_keys(self, check_keys, pressed_keys):
		for index, key in enumerate(check_keys):
			if not pressed_keys[self.key_dict[key]]:
				if index > 0:
					print(key, " was not found, number: ", self.key_dict[key], ", is_pressed: ", pressed_keys[self.key_dict[key]])
					print("pressed keys: ", [pygame.key.name(i) for i,k in enumerate(pressed_keys) if k] )
				return False
		print(check_keys," is pressed")
		self.game.keys_down = check_keys 
		return True

	def init_key_dict(self):
		all_keys = pygame.key.get_pressed()
		key_dict = {}
		for key_num, is_key_pressed in enumerate(all_keys):
			key_dict[pygame.key.name(key_num)] = key_num
		return key_dict

	def run(self, move_direction ):
		if self.is_grounded:
			delta_velocity = numpy.multiply( move_direction, self.run_acceleration)
			self.add_velocity( delta_velocity )
			if self.game.move_screen:
				print("running and moving screen")
				self.game.display_move_delta=move_direction

	def jump(self):
		if self.is_grounded:
			self.add_velocity( self.jump_velocity )
			self.is_grounded = False

	def add_velocity(self, delta_velocity):
		self.velocity = numpy.add(self.velocity, delta_velocity)
		self.clamp_velocity() 

	def clamp_velocity(self):
		for index, value in enumerate(self.velocity):
			self.velocity[index] = max( self.max_velocity[index] * -1, min( self.max_velocity[index], self.velocity[index]) )

	def update_position(self):
		self.rect.center = numpy.add(self.rect.center, self.velocity)

	def apply_gravity(self):
		if not self.is_grounded:
			self.add_velocity( self.gravity )

	def apply_friction(self):
		friction_direction = self.gravity.index(min( numpy.absolute(self.gravity) ))
		if self.is_grounded and self.velocity[friction_direction] != 0:
			friction = [0, 0]
			friction[friction_direction] = -1 * numpy.sign(self.velocity[friction_direction]) * self.friction
			self.add_velocity( friction )

	def check_collision(self):
		collided_sprite = pygame.sprite.spritecollideany(self, self.game.level_maker)
		
		if collided_sprite:
			if collided_sprite in self.game.goals:
				self.game.levelup()
			elif collided_sprite in self.game.killers:
				self.kill()
			else:
				self.bounce_out(collided_sprite)
		else:
			self.is_grounded = False

	def bounce_out(self, collided_sprite):
		penetration_distances = self.rect.clip(collided_sprite.rect).size
		exit_axis = penetration_distances.index(min(penetration_distances))
		
		exit_vector = [0, 0]
		exit_sign = numpy.sign(self.rect.center[exit_axis] - collided_sprite.rect.center[exit_axis])
		exit_vector[exit_axis] = exit_sign * penetration_distances[exit_axis]
		self.rect = self.rect.move(exit_vector)
		self.velocity[exit_axis] = 0

		if exit_axis == self.gravity.index(max( numpy.absolute(self.gravity) )):
			self.is_grounded = True
