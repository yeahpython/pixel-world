import pygame
from pygame import draw, Surface, Rect, key, K_RIGHT, K_LEFT, K_UP, K_DOWN
from math import cos, sin, floor
import random
from Queue import PriorityQueue

game_title = "pixel world"
black = (0, 0, 0)

green = (0, 255, 0)
transparent = (100, 200, 100)

white = (255, 255, 255)
alphawhite = (255, 255, 255, 255)

'''
blue = (200, 0, 205)
alphablue = (200, 0, 205, 255)

monster = (255, 0, 0)
alphamonster = (255, 0, 0, 255)

mystery = (255, 100, 0)
alphamystery = (255, 100, 0, 255)

tower = (0, 255, 0)
alphatower = (0, 255, 0, 255)

blaze = (255, 0, 50)
alphablaze = (255, 0, 50, 255)

sky = (255, 170, 0)'''


#################################


blue = (200, 200, 200)
alphablue = (200, 200, 200, 255)

monster = (144, 144, 144)
alphamonster = (144, 144, 144, 255)

mystery = (120, 120, 120)
alphamystery = (120, 120, 120, 255)

tower = (180, 180, 180)
alphatower = (180, 180, 180, 255)

blaze = (10, 10, 10)
alphablaze = (10, 10, 10, 255)

sky = (254, 254, 254)


##################################


'''blue = (200, 200, 200)
alphablue = (200, 200, 200, 255)

monster = (144, 144, 144)
alphamonster = (144, 144, 144, 255)

mystery = (120, 120, 120)
alphamystery = (120, 120, 120, 255)

tower = (180, 180, 180)
alphatower = (180, 180, 180, 255)

blaze = (10, 10, 10)
alphablaze = (10, 10, 10, 255)

sky = (0,0,0)'''

SOLID_COLORS = (alphawhite, alphablue, alphamonster, alphamystery, alphatower, alphablaze)



UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DRAW_ACTORS = True


screen_w = 800
screen_h = 600
screen_size = (screen_w, screen_h)

def initialization():
	pygame.init()
	pygame.display.set_mode(screen_size)
	pygame.display.set_caption(game_title)

def main_loop():

	'''these things only need to happen once'''
	screen = pygame.display.get_surface()
	

	clock = pygame.time.Clock()
	dt=0
	font = pygame.font.Font(None, 30)
	while 1:
		world = World(screen.get_size())
		physicals = []
		#for k in range(1, 16):
		#	p = Loop( [(-5*k, -5*k), (0, 0), (5*k, -5*k)], 5 * k, 200 + 10 * k)
		#	physicals.append(p)

		p = Player(random.randrange(101, world.width - 1), world.height - 200)
		physicals.append(p)

		q = WaterWalker2(random.randrange(101, world.width - 1), world.height - 100)
		physicals.append(q)

		q1 = WaterWalker(random.randrange(101, world.width - 1), world.height - 100)
		physicals.append(q1)

		r = TowerBuilder(random.randrange(0, world.width - 1), world.height - 100)
		physicals.append(r)

		s = Mystery(random.randrange(0, world.width - 1), world.height - 100)
		physicals.append(s)

		#t = Monster(random.randrange(0, world.width - 1), world.height - 100)
		#physicals.append(t)

		i = 0
		for i in range(10000):
			dt = clock.tick(10000)
			#world.update(dt)
			world.render_to(screen)
			for physical in physicals:
				if physical.visible and not physical.has_physics:
					physical.render_to(screen)
			for physical in physicals:
				if physical.visible and physical.has_physics:
					physical.update_physics(world.background)
					physical.render_to(screen)
			pygame.display.flip()
			pygame.event.pump()

			if pygame.event.get(pygame.QUIT):
				return 0

			if pygame.mouse.get_pressed()[2]:
				break

			if pygame.mouse.get_pressed()[1]:
				q.x, q.y = pygame.mouse.get_pos()
				q.active = True

			if pygame.mouse.get_pressed()[0]:
				x,y = pygame.mouse.get_pos()
				world.add_blob(x, y)

			#if pygame.key.get_pressed()[pygame.K_x]:
			#	world.add_blob(p.x, p.y, black = 1)
			#if pygame.key.get_pressed()[pygame.K_z]:
			#	world.add_blob(p.x, p.y + 10, black = 0)
		#clock.tick(0.2)

class World(object):
	def __init__(self, size):
		self.background = Surface(size)
		self.size = size
		self.width, self.height = size
		draw.circle(self.background, white, (400, self.height - 110), 40, 0)
		draw.circle(self.background, black, (400, self.height - 110), 38, 0)
		draw.circle(self.background, white, (400, self.height - 110), 20, 0)
		draw.circle(self.background, black, (400, self.height - 130), 10, 0)
		
		#points = ((0, self.height - 200), ( 100, self.height - 100), (0, self.height -100))
		#draw.polygon(self.background, white, points)
		rect = Rect(0, self.height - 100, self.width, 100)
		self.background.fill(sky)
		draw.rect(self.background, blue, rect)

	def render_to(self, screen):
		screen.blit(self.background, (0,0))

	def add_blob(self, x, y, black = 0):
		if not black:
			draw.circle(self.background, white, (x, y), 20, 0)
		else:
			draw.circle(self.background, black, (x, y), 20, 0)

class Physical(object):
	def __init__(self, x = None, y = None):
		self.x, self.y = x, y
		if self.x == None:
			self.x = screen_w /2
			self.y = screen_w /2
		self.visible = 0
		self.has_physics = False

class VisiblePhysical(Physical):
	def __init__(self, x = None, y = None):
		super(VisiblePhysical, self).__init__(x, y)
		self.visible = 1
	
	def render_to(self, screen):
		draw.circle(screen, white, (self.x, self.y), 10, 1)

class Loop(VisiblePhysical):
	def __init__(self, points, x = None, y = None):
		super(Loop, self).__init__(x, y)
		self.points = None
		self.x_buffer = None
		self.y_buffer = None
		self.buffer = None
		self.update_shape(points)

	def escape_up(self, screen):
		while True:
			if screen.get_rect().collidepoint(self.x, self.y) and tuple(screen.get_at((self.x, self.y))) in SOLID_COLORS:
				self.y -= 1
			else:
				break

	def update_shape(self, points):
		self.points = points
		self.update_buffer()
		
	def update_buffer(self):
		w_buffer = max(x for x, y in self.points) - min(x for x, y in self.points) + 1
		h_buffer = max(y for x, y in self.points) - min(y for x, y in self.points) + 1
		self.x_buffer = - min(x for x, y in self.points)
		self.y_buffer = - min(y for x, y in self.points)
		self.buffer = Surface((w_buffer, h_buffer))
		self.buffer.set_colorkey(transparent)
		self.buffer.fill(transparent)
		offset_points = [(x + self.x_buffer, y + self.y_buffer) for x, y in self.points]
		#draw.polygon(self.buffer, white, offset_points)
		draw.lines(self.buffer, white, True, offset_points)

	def render_to(self, screen):
		if DRAW_ACTORS:
			screen.blit(self.buffer, (self.x - self.x_buffer, self.y - self.y_buffer))

	def try_move(self, moves, screen):
		x = self.x
		y = self.y
		for dx, dy in moves:
			x += dx
			y += dy
			if not is_free(x, y, screen):
				return False

		self.x = x
		self.y = y
		return True

	def check_offset(self, dx, dy, screen):
		return is_free(self.x + dx, self.y + dy, screen)

K_MAX_JETPACK = 60

class TowerBuilder(Loop):
	def __init__(self, x = None, y = None):
		super(TowerBuilder, self).__init__([(0,-5), (0,0), (0, -5), (2, -7), (0, -9), (-2, -7)], x, y)
		self.has_physics = True
		self.active = True
		self.height = 0
		self.stun = 0
		self.prefered = RIGHT
		self.less_prefered = LEFT
		self.threshold = random.randrange(20, 80)
		self.color = tower

	def update_physics(self, screen):
		if self.active:
			self.physics_step(screen, 5)

	def physics_step(self, screen, n):
		for i in range(n):
			self.escape_up(screen)
			x, y = self.x, self.y
			
			if self.stun:
				if not self.try_move((self.prefered,), screen):
					self.prefered, self.less_prefered = self.less_prefered, self.prefered
				self.stun -= 1
				screen.set_at((x, y), self.color)
				self.height = 0
			elif self.try_move((DOWN,), screen):
				pass
			elif self.height < self.threshold and self.try_move((UP,), screen):
				screen.set_at((x, y), self.color)
				self.height += 1
			else:
				self.stun = random.randrange(2, 20)# used to be 2, 20
				self.threshold = random.randrange(5, 30) #used to be 5, 30


			

class WaterWalker(Loop):
	def __init__(self, x = None, y = None):
		super(WaterWalker, self).__init__([(-5,-5), (0,0), (5, -5), (0, -15)], x, y)
		self.has_physics = True
		self.prefered = RIGHT
		self.less_prefered = LEFT
		self.backup = (self.x, self.y)
		self.active = True
		self.color = blaze

	def update_physics(self, screen):
		if self.active:
			self.physics_step(screen, 5)

	def physics_step(self, screen, n):
		for i in range(n):
			x, y = self.x, self.y
			if self.try_move((DOWN,), screen):
				self.try_move((DOWN, DOWN), screen)
			else:
				
				
				if self.try_move((self.prefered,), screen):
					if self.check_offset(-self.prefered[0], -1, screen):
						self.backup = (self.x - self.prefered[0], self.y - 1)
						#screen.set_at(self.backup, green)
				elif self.try_move((self.less_prefered,), screen):
					if self.check_offset(-self.less_prefered[0], -1, screen):
						self.backup = (self.x - self.less_prefered[0], self.y - 1)
						#screen.set_at(self.backup, green)
					self.less_prefered, self.prefered = self.prefered, self.less_prefered
				elif self.try_move((UP,), screen):
					self.less_prefered, self.prefered = self.prefered, self.less_prefered
				else:
					self.x, self.y = self.backup
					self.escape_up(screen)
					if not self.check_offset(0, 0, screen):
						self.active = False
			screen.set_at((x, y), self.color)

class WaterWalker2(Loop):
	def __init__(self, x = None, y = None):
		super(WaterWalker2, self).__init__([(-5,-5), (0,0), (5, -5), (0, -15)], x, y)
		self.has_physics = True
		self.prefered = RIGHT
		self.less_prefered = LEFT
		self.backup = (self.x, self.y)
		self.active = True
		self.backups = PriorityQueue()

	def update_physics(self, screen):
		if self.active:
			self.physics_step_new(screen, 3)

	'''def physics_step(self, screen, n):
		for i in range(n):
			#if self.y < self.backup[1]:
			#	self.x, self.y = self.backup
			x, y = self.x, self.y
			if self.try_move((DOWN,), screen):
				self.try_move((DOWN, DOWN), screen)
			else:
				if self.check_offset(0, -1, screen) and self.y > self.backup[1]:
					self.backup = self.x, self.y + 1

				if self.try_move((self.prefered,), screen):
					if self.check_offset(-self.prefered[0], -1, screen):
						if self.y - 1 < self.backup[0]:
							self.backup = (self.x - self.prefered[0], self.y - 1)
						#screen.set_at(self.backup, green)
				elif self.try_move((self.less_prefered,), screen):
					if self.check_offset(-self.less_prefered[0], -1, screen):
						if self.y - 1 < self.backup[0]:
							self.backup = (self.x - self.less_prefered[0], self.y - 1)
						#screen.set_at(self.backup, green)
					self.less_prefered, self.prefered = self.prefered, self.less_prefered
				elif self.try_move((UP, self.less_prefered), screen) or self.try_move((UP,), screen):
					pass
					#self.less_prefered, self.prefered = self.prefered, self.less_prefered
				else:
					self.x, self.y = self.backup
					self.escape_up(screen)
					self.less_prefered, self.prefered = self.prefered, self.less_prefered
					if not self.check_offset(0, 0, screen):
						self.active = False
			screen.set_at((x, y), white)'''

	def physics_step_new(self, screen, n):
		
		for i in range(n):
			if not self.active:
				return
			if self.backups.qsize() and -self.y > self.backups.queue[0][0]:
				temp_x, temp_y = self.x, self.y
				self.x, self.y = self.backups.get()[1]
				self.backups.put( (-temp_y, (temp_x, temp_y)))
				#screen.set_at((temp_x, temp_y), green)
			x, y = self.x, self.y
			if self.try_move((DOWN,), screen) or self.try_move((self.prefered, DOWN), screen) or self.try_move((self.less_prefered, DOWN), screen):
				pass
			elif self.try_move((self.less_prefered,), screen):
				pass
			#
			#  #V  no fall
			#   #
			else:
				screen.set_at((x, y), blue)
				if self.try_move((self.prefered,), screen):
					# ???
					# #V?
					# ##?
					if not self.check_offset(0, -1, screen):
						# ?#?
						# #V?
						# ##?
						#self.backups.append((self.x + self.less_prefered[0], self.y -1))
						self.backups.put((-1 *(self.y - 1), (self.x + self.less_prefered[0], self.y -1)))
						#screen.set_at((self.x + self.less_prefered[0], self.y -1), green)
						# *#?
						# #V?
						# ##?
				elif self.try_move((UP,), screen):
					pass
				else:
					#trapped
					if self.backups.empty():
						print self.x, self.y
						try:
							print screen.get_at((self.x, self.y))
						except:
							print "could not get color"
						print "dead"
						self.active = 0
					else:
						self.x, self.y = self.backups.get()[1]


class Mystery(WaterWalker):
	def __init__(self, x = None, y = None):
		super(Mystery, self).__init__(x, y)
		self.has_physics = True
		self.active = True
		self.home = None
		self.color = mystery

	def update_physics(self, screen):
		if self.active:
			x, y = self.x, self.y
			if not self.home:
				if self.try_move((DOWN,), screen):
					pass
				else:
					self.home = self.x, self.y
			else:
				self.home = random.randrange(-3, 4) + self.home[0], random.randrange(-3, 4) + self.home[1]
				self.try_move((UP, UP, UP, UP, UP, UP, UP), screen)
				super(Mystery, self).update_physics(screen)

class Monster(WaterWalker):
	def __init__(self, x = None, y = None):
		super(Monster, self).__init__(x, y)
		self.has_physics = True
		self.active = True
		self.home = None
		self.color = monster

	def update_physics(self, screen):
		if self.active:
			x, y = self.x, self.y
			if not self.home:
				if self.try_move((DOWN,), screen):
					pass
				else:
					self.home = self.x, self.y
			else:
				self.home = random.randrange(-3, 4) + self.home[0], random.randrange(-3, 4) + self.home[1]
				self.x, self.y = self.home
				#self.try_move((UP, UP, UP, UP, UP, UP, UP), screen)
				super(Monster, self).update_physics(screen)

class Player(Loop):
	def __init__(self, x = None, y = None):
		super(Player, self).__init__([(-5,-10), (0,0), (5, -10)], x, y)
		self.has_physics = True
		self.jetpack = 0 + K_MAX_JETPACK
		self.vx = 0
		self.vy = 0

	def update_physics(self, screen):
		self.escape_up(screen)
		for i in range(2):
			if screen.get_rect().collidepoint(self.x, self.y + 2) and tuple(screen.get_at((self.x, self.y + 1))) != (255, 255, 255, 255):
				if not (key.get_pressed()[K_UP] and self.jetpack): 
					self.y += 1
					self.jetpack = 0
			else:
				self.jetpack = K_MAX_JETPACK
				if not key.get_pressed()[K_RIGHT] and not key.get_pressed()[K_LEFT]:
					self.vx = 0

		if key.get_pressed()[K_RIGHT]:
			self.vx += 0.2
			if self.vx > 4:
				self.vx = 4
		if key.get_pressed()[K_LEFT]:
			self.vx -= 0.2
			if self.vx < -4:
				self.vx = -4

		if self.vx > 0:
			for i in range(int(self.vx)):
				if self.try_move((RIGHT,), screen):
					pass
				elif self.try_move((UP, RIGHT), screen):
					pass
				else:
					self.vx = 0
					break
		if self.vx < 0:
			for i in range(int(-self.vx)):
				if self.try_move((LEFT,), screen):
					pass
				elif self.try_move((UP, LEFT), screen):
					pass
				else:
					self.vx = 0
					break
		if key.get_pressed()[K_UP] and self.jetpack:
			#if screen.get_rect().contains(Rect(self.x - 5, self.y - 12, 11, 2)) and all(tuple(screen.get_at((self.x + i, self.y - 12))) != (255, 255, 255, 255) for i in range(-5, 6)):
			
			for i in range(2):
				if self.try_move((UP,), screen):
					self.jetpack -= 1
					if self.jetpack < 0:
						self.jetpack = 0
				else:
					self.jetpack = 0

	

	



def is_free(x, y, screen):
		return screen.get_rect().collidepoint(x, y) and tuple(screen.get_at((x, y))) not in SOLID_COLORS

def main():
	initialization()

	pygame.event.set_blocked(None)
	pygame.event.set_allowed(pygame.QUIT)

	main_loop()