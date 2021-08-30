import pygame, os
APP_PATH = os.path.dirname(os.path.realpath(__file__)) + os.sep

class Ruoka(pygame.sprite.Sprite):
	def __init__(self, tileMap, pos):
		pygame.sprite.Sprite.__init__(self)
		for x, y, gid, in tileMap.get_layer_by_name("ruoka"):
			image = tileMap.get_tile_image_by_gid(gid)
			if image:
				self.image = image
				break
		self.rect = self.image.get_rect()
		self.rect.center = pos