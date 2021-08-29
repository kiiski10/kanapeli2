import pygame, os, math
from core import screenPosToTilePos, tilePosToScreenPos

APP_PATH = os.path.dirname(os.path.realpath(__file__))

class Kana(pygame.sprite.Sprite):
	def __init__(self, posX, posY, tileMap):
		self.state = "LOADING"
		self.munat = []
		self.world = tileMap
		pygame.sprite.Sprite.__init__(self)
		self.image_up = pygame.image.load(os.path.join(APP_PATH, "img", "pienet", "kana-up.png"))
		self.image_down = pygame.image.load(os.path.join(APP_PATH, "img", "pienet", "kana-down.png"))
		self.image_left = pygame.image.load(os.path.join(APP_PATH, "img", "pienet", "kana-left.png"))
		self.image_right = pygame.image.load(os.path.join(APP_PATH, "img", "pienet", "kana-right.png"))
		self.image = self.image_right
		self.rect = self.image.get_rect()
		self.rect.center = [posX, posY]
		self.location = self.rect.center
		self.targetTile = screenPosToTilePos(self, self.world, self.rect.center)
		self.lastPos = self.rect.center
		self.maxSpeed = 2

	def hitReaction(self):
		self.state = "BOUNCING"
		angle = self.coordsToDistAngle(self.rect.center)[1]
		movement = pygame.math.Vector2()
		movement.from_polar((10, angle - 195))
		movement.x = int(movement.x)
		movement.y = int(movement.y)
		self.targetPos = movement + self.location

	def move(self, distance, degrees):
		movement = pygame.math.Vector2()
		if self.state == "BOUNCING":
			if distance > self.maxSpeed * 3:
				distance = self.maxSpeed * 3
		else:
			if distance > self.maxSpeed:
				distance = self.maxSpeed

		movement.from_polar((distance, degrees))
		self.location += movement
		self.rect.center = self.location

		if self.state == "MOVING":
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
		distance, degrees = self.coordsToDistAngle(tilePosToScreenPos(self, self.world, self.targetTile))
		self.move(distance, degrees)