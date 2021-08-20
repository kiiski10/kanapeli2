import pygame, os, math

APP_PATH = os.path.dirname(os.path.realpath(__file__))

class Kana(pygame.sprite.Sprite):
	def __init__(self, posX, posY):
		self.munat = []
		pygame.sprite.Sprite.__init__(self)
		self.image_up = pygame.image.load(os.path.join(APP_PATH, "img", "pienet", "kana-up.png"))
		self.image_down = pygame.image.load(os.path.join(APP_PATH, "img", "pienet", "kana-down.png"))
		self.image_left = pygame.image.load(os.path.join(APP_PATH, "img", "pienet", "kana-left.png"))
		self.image_right = pygame.image.load(os.path.join(APP_PATH, "img", "pienet", "kana-right.png"))
		self.image = self.image_right
		self.rect = self.image.get_rect()
		self.rect.center = [posX, posY]
		self.location = self.rect.center
		self.targetPos = self.rect.center
		self.lastPos = self.rect.center
		self.maxSpeed = 1

	def hitReaction(self):
		print("im hit:", self.location, self.rect.center, self.coordsToDistAngle(self.rect.center))
		self.targetPos = self.location

	def move(self, distance, degrees, turnImage=True):
		movement = pygame.math.Vector2()
		if distance > self.maxSpeed:
			distance = self.maxSpeed

		movement.from_polar((distance, degrees))
		self.location += movement
		self.rect.center = self.location

		if turnImage:
			if degrees > 45 and degrees < 145:
				self.image = self.image_down
			elif degrees > -145 and degrees < -45:
				self.image = self.image_up
			elif degrees > -45 and degrees < 45:
				self.image = self.image_right
			elif degrees > 145 or degrees < -145:
				self.image = self.image_left

	def coordsToDistAngle(self, target):
		f = pygame.math.Vector2(self.location)
		t = pygame.math.Vector2(target)
		rad = math.atan2(t.y - f.y, t.x - f.x)
		distance = t.distance_to(f)
		degrees = math.degrees(rad)
		return(distance, degrees)

	def update(self):
		distance, degrees = self.coordsToDistAngle(self.targetPos)
		self.move(distance, degrees)