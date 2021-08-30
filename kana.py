import pygame, os, math, time
from core import screenPosToTilePos, tilePosToScreenPos

APP_PATH = os.path.dirname(os.path.realpath(__file__))

class Kana(pygame.sprite.Sprite):
	def __init__(self, posX, posY, game):
		self.state = "LOADING"
		self.munat = []
		self.game = game
		self.world = self.game.tileMap
		pygame.sprite.Sprite.__init__(self)

		self.image_left = self.loadCharacterTiles("kana-left")
		self.image_right = self.loadCharacterTiles("kana-right")
		self.image_down = self.loadCharacterTiles("kana-front")
		self.image_up = self.loadCharacterTiles("kana-back")
		self.image = self.image_left
		self.rect = self.image.get_rect()
		self.rect.center = [posX, posY]
		self.location = self.rect.center
		self.targetTile = None
		self.targetQue = []
		self.lastPos = self.rect.center
		self.lastMoveTime = time.time()
		self.speed = 80

	def loadCharacterTiles(self, layerName):
		wholeCharacter = pygame.Surface(
			(
				self.world.tileheight,
				self.world.tileheight * 2
			),
			pygame.SRCALPHA,
			16
		)
		pos = 0
		for x, y, gid, in self.world.get_layer_by_name(layerName):
			image = self.world.get_tile_image_by_gid(gid)
			if image:
				wholeCharacter.blit(image, (0, pos))
				pos += self.world.tileheight
		return wholeCharacter


	def hitReaction(self):
		self.state = "BOUNCING"
		angle = self.coordsToDistAngle(self.rect.center)[1]
		movement = pygame.math.Vector2()
		movement.from_polar((25, angle - 195))
		movement.x = int(movement.x)
		movement.y = int(movement.y)
		self.lastMoveTime = time.time()
		self.location = movement + self.location
		self.targetQue = []
		self.targetTile = None


	def move(self, distance, degrees):
		movement = pygame.math.Vector2()

		now = time.time()
		dt = now - self.lastMoveTime
		self.lastMoveTime = time.time()
		distance = self.speed * dt

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